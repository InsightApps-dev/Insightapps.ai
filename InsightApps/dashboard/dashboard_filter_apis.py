from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from dashboard.views import test_token
import psycopg2,cx_Oracle
from dashboard import models,serializers    
import pandas as pd
from sqlalchemy import text,inspect
import numpy as np
from .models import *
import ast,re,itertools
from datetime import datetime
import boto3
import json
import requests
from project import settings
import io
from dashboard.columns_extract import server_connection
from django.core.paginator import Paginator
import sqlglot
import logging
from dashboard import roles,previlages
from .Filters import connection_data_retrieve,server_details_check

quotes = {
    'postgresql': ('"', '"'),
    'oracle': ('"', '"'),
    'mysql': ('`', '`'),
    'sqlite': ('"', '"'),
    'microsoftsqlserver': ('[', ']'),
    'snowflake': ('', '')
}
date_format_syntaxes = {
    'postgresql': lambda column: f"""to_char("{str(column)}", 'yyyy-mm-dd')""",
    'oracle': lambda column: f"""TO_CHAR("{str(column)}", 'YYYY-MM-DD')""",
    'mysql': lambda column: f"""DATE_FORMAT(`{str(column)}`, '%Y-%m-%d')""",
    'sqlite': lambda column: f"""strftime('%Y-%m-%d', "{str(column)}")""",
    'microsoftsqlserver': lambda column: f"""FORMAT([{str(column)}], 'yyyy-MM-dd')""",
    'snowflake': lambda column: f"""TO_CHAR({str(column)}, 'YYYY-MM-DD')"""
}


class DashboardQuerySetList(CreateAPIView):
    serializer_class = serializers.dashboard_querysetname_preview

    def post(self, request, token):
        tok1 = test_token(token)
        if tok1['status'] != 200:
            return Response({"message": tok1['message']}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        dashboard_id = serializer.validated_data["dashboard_id"]
        if not dashboard_id:
            return Response({"message": "Dashboard ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not dashboard_data.objects.filter(id=dashboard_id).exists():
            return Response({"message": "Dashboard not found"}, status=status.HTTP_404_NOT_FOUND)

        dashboard = dashboard_data.objects.get(id=dashboard_id)
        
        queryset_ids1 = eval(dashboard.queryset_id)
        queryset_ids = list(set(queryset_ids1))
        sheet_ids = dashboard.sheet_ids
       
        data = []

        if isinstance(queryset_ids, str):
            try:
                queryset_ids = eval(queryset_ids)
            except (SyntaxError, NameError):
                return Response({"message": "Invalid queryset_ids format"}, status=status.HTTP_400_BAD_REQUEST)
                
        if isinstance(sheet_ids, str):
            try:
                sheet_ids = eval(sheet_ids)
            except (SyntaxError, NameError):
                return Response({"message": "Invalid sheet_ids format"}, status=status.HTTP_400_BAD_REQUEST)

        queryset_names = []

        for i in queryset_ids:
            try:
                m = QuerySets.objects.get(queryset_id=i).query_name
                queryset_names.append(m)
                data.append({
                    "dashboard_id": dashboard.id,
                    "queryset_id": i,
                    "queryset_name": m
                    # "sheet_ids": sheet_ids
                })
            except QuerySets.DoesNotExist:
                return Response({"message": f"QuerySet with id {i} not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
        return Response(data, status=status.HTTP_200_OK)

class DashboardQSColumnAndSheetsPreview(CreateAPIView):
    serializer_class = serializers.DashboardpreviewSerializer

    def post(self, request, token):
        tok1 = test_token(token)
        if tok1['status'] != 200:
            return Response({"message": tok1['message']}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'serializer error'}, status=status.HTTP_404_NOT_FOUND)
        
        dashboard_id = serializer.validated_data["dashboard_id"]
        query_id = serializer.validated_data["queryset_id"]
        user_id = tok1['user_id']

        if not dashboard_data.objects.filter(id=dashboard_id).exists():
            return Response({'message': "Invalid Dashboard ID"}, status=status.HTTP_404_NOT_FOUND)
        
        database_id,file_id,joining_tables,custom = get_server_id(query_id)
    
        sheet_names = []

        f = get_dashboard_sheets(dashboard_id,query_id)
        for i in f:
            sheet_names.append({"id": sheet_data.objects.get(id=i).id, "name": sheet_data.objects.get(id=i).sheet_name})
        
        try:
            # database_id = 478
            con_data =connection_data_retrieve(database_id,file_id,user_id)
            if con_data['status'] ==200:                
                ServerType1 = con_data['serverType1']
                server_details = con_data['server_details']
                file_type = con_data["file_type"]
                file_data =con_data["file_data"]
                dtype = con_data['dbtype']

            else:
                return Response({'message':con_data['message']},status = status.HTTP_404_NOT_FOUND)
            serdt=server_details_check(ServerType1,server_details,file_type,file_data,eval(joining_tables),custom)
            if serdt['status']==200:
                engine=serdt['engine']
                cursor=serdt['cursor']
            else:
                return Response({'message':serdt['message']},status=serdt['status'])
        except ServerDetails.DoesNotExist:
            return Response({'message': 'Server details not found'}, status=status.HTTP_404_NOT_FOUND)
        except ServerType.DoesNotExist:
            return Response({'message': 'Server type not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            qr = ''
            # q_id = dashboard_data.objects.get(id=dashboard_id, user_id=user_id)
            # query_id = q_id.queryset_id
            joining = QuerySets.objects.get(queryset_id=query_id, user_id=user_id)
            query_set = joining.custom_query
            try:
                datasource_id = DataSource_querysets.objects.get(queryset_id=query_id, user_id=user_id)
                datasource_query = datasource_id.custom_query
                qr += datasource_query
            except:
                qr += query_set
            data = cursor.execute(text(qr))
            if dtype.lower()== "microsoftsqlserver":
                samp = cursor.description
                columns_list = [
                {
                    "column_name": col[0],
                    "column_dtype": col[0].__name__
                }
                for col in samp
            ]
            else:
                samp = data.cursor.description
                type_code_to_name = get_columns_list(samp, dtype)
                    
                columns_list = [
                    {
                        "column_name": col[0],
                        "column_dtype": type_code_to_name.get(col[1], 'string')
                    }
                    for col in samp
                ]
        

            response_data = {
                "columns": columns_list,
            }
            return Response({"response_data": response_data, "sheets": sheet_names, "dashboard_id": dashboard_id, "server_id": database_id,"query_id":query_id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

        

        
def get_dashboard_sheets(dashboard_id, query_id):
    try:
        dd = dashboard_data.objects.get(id=dashboard_id)

        sheet_ids = []

        s = eval(dd.sheet_ids) if isinstance(dd.sheet_ids, str) else dd.sheet_ids
        
        for i in s:
            try:
                m = sheet_data.objects.get(id=i, queryset_id=query_id)
                sheet_ids.append(m.id)
            except sheet_data.DoesNotExist:
                continue
        
        return sheet_ids
    
    except dashboard_data.DoesNotExist:
        return Response({"message": "Invalid Dashboard ID"}, status=status.HTTP_404_NOT_FOUND)
        
class DashboardFilterSave(CreateAPIView):
    serializer_class = serializers.Dashboardfilter_save
    def post(self, request, token):
        role_list=roles.get_previlage_id(previlage=[previlages.create_dashboard_filter])
        tok1 = roles.role_status(token,role_list)
        if tok1['status'] != 200:
            return Response({"message": tok1['message']}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'serializer error'}, status=status.HTTP_204_NO_CONTENT)
        
        dashboard_id = serializer.validated_data["dashboard_id"]
        filter_name = serializer.validated_data["filter_name"]
        selected_column = serializer.validated_data["column"]
        sheets = serializer.validated_data["sheets"]
        datatype = serializer.validated_data["datatype"]
        queryset_id = serializer.validated_data["queryset_id"]       
        user_id = tok1['user_id']
        if dashboard_data.objects.filter(id = dashboard_id,user_id=user_id).exists():
           
            dash_filter = DashboardFilters.objects.create(
                user_id = user_id,
                dashboard_id = dashboard_id,
                sheet_id_list = sheets,
                filter_name = filter_name,
                column_name = selected_column,
                column_datatype = datatype,
                queryset_id = queryset_id
            )
            
            return Response({"dashboard_filter_id":dash_filter.id,
                            "dashboard_id":dashboard_id,
                            "filter_name":filter_name,
                            "selected_column":selected_column,
                            "sheets":sheets,
                            "datatype":datatype,
                            "queryset_id":queryset_id
                            })
        else:
            return Response({"message":"dashboard id not found"},status=status.HTTP_404_NOT_FOUND)
    
    serializer_get_clas = serializers.Dashboard_datapreviewSerializer
    def get(self,request,token):
        
        tok1 = test_token(token)
        if tok1['status'] != 200:
            return Response({"message": tok1['message']}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_get_clas(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'serializer error'}, status=status.HTTP_204_NO_CONTENT)
        
        filter_id = serializer.validated_data["id"]
        if DashboardFilters.objects.filter(id= filter_id).exists():
            dash_filter = DashboardFilters.objects.get(id= filter_id)
            return Response({"dashboard_filter_id":dash_filter.id,
                                "dashboard_id":dash_filter.dashboard_id,
                                "filter_name":dash_filter.filter_name,
                                "selected_column":dash_filter.column_name,
                                "sheets":dash_filter.sheet_id_list,
                                "datatype":dash_filter.column_datatype
                                })
        else:
            return Response({"message":"dashboard filter id not found"},status=status.HTTP_404_NOT_FOUND)
        
    serializer_put_class = serializers.Dashboardfilter_save
    def put(self, request, token):
        role_list=roles.get_previlage_id(previlage=[previlages.edit_dashboard_filter])
        tok1 = roles.role_status(token,role_list)
        if tok1['status'] != 200:
            return Response({"message": tok1['message']}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_put_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'serializer error'}, status=status.HTTP_204_NO_CONTENT)
        
        dashboard_filter_id = serializer.validated_data["dashboard_filter_id"]
        dashboard_id = serializer.validated_data["dashboard_id"]
        filter_name = serializer.validated_data["filter_name"]
        selected_column = serializer.validated_data["column"]
        sheets = serializer.validated_data["sheets"]
        datatype = serializer.validated_data["datatype"]
        queryset_id = serializer.validated_data["queryset_id"]       
        user_id = tok1['user_id']
        if not DashboardFilters.objects.filter(id = dashboard_filter_id).exists():
            return Response({"message":"dashboard filter id not found"},status=status.HTTP_404_NOT_FOUND)
        
        if dashboard_data.objects.filter(id = dashboard_id,user_id=user_id).exists():
            DashboardFilters.objects.filter(
                id = dashboard_filter_id
                ).update(
                user_id = user_id,
                dashboard_id = dashboard_id,
                sheet_id_list = sheets,
                filter_name = filter_name,
                column_name = selected_column,
                column_datatype = datatype,
                queryset_id = queryset_id,
                updated_at = datetime.now()
            )

            return Response({"dashboard_filter_id":dashboard_filter_id,
                            "dashboard_id":dashboard_id,
                            "filter_name":filter_name,
                            "selected_column":selected_column,
                            "sheets":sheets,
                            "datatype":datatype,
                            "queryset_id":queryset_id
                            })
        else:
            return Response({"message":"dashboard id not found"},status=status.HTTP_404_NOT_FOUND)
        


        
class DashboardFilterColumnDataPreview(CreateAPIView):
    serializer_class = serializers.Dashboard_datapreviewSerializer
    def post(self, request, token):
        if token==settings.DEFAULT_TOKEN:
            tok_status=200
        else:
            tok1 = test_token(token)
            tok_status=tok1['status']
        if tok_status !=200:
            return Response({"message": tok1['message']}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'serializer error'}, status=status.HTTP_204_NO_CONTENT)
        filter_id = serializer.validated_data["id"]
        search_term = serializer.validated_data["search"]
        if not DashboardFilters.objects.filter(id = filter_id).exists():
            return Response({'message':"Invalid Dashboard Filter ID"},status=status.HTTP_404_NOT_FOUND)
        
        if not dashboard_data.objects.filter(id = DashboardFilters.objects.get(id = filter_id).dashboard_id).exists():
            return Response({'message':"Invalid Dashboard ID"},status=status.HTTP_404_NOT_FOUND)
        query_id = DashboardFilters.objects.get(id = filter_id).queryset_id
        dashboard_id = DashboardFilters.objects.get(id = filter_id).dashboard_id
        database_id = get_server_id(query_id)
        column = DashboardFilters.objects.get(id = filter_id).column_name
        datatype = DashboardFilters.objects.get(id = filter_id).column_datatype
        database_id,file_id,joining_tables,custom = get_server_id(query_id)
        
        if token==settings.DEFAULT_TOKEN:
            dashboarddata=dashboard_data.objects.get(id=dashboard_id)
            user_id=dashboarddata.user_id
        else:
            user_id = tok1['user_id']
        try:
            con_data =connection_data_retrieve(database_id,file_id,user_id)
            if con_data['status'] ==200:                
                ServerType1 = con_data['serverType1']
                server_details = con_data['server_details']
                file_type = con_data["file_type"]
                file_data =con_data["file_data"]
                dtype = con_data['dbtype']
            else:
                return Response({'message':con_data['message']},status = status.HTTP_404_NOT_FOUND)
            
            serdt=server_details_check(ServerType1,server_details,file_type,file_data,eval(joining_tables),custom)
            if serdt['status']==200:
                engine=serdt['engine']
                cursor=serdt['cursor']
            else:
                return Response({'message':serdt['message']},status=serdt['status'])
            
        except ServerDetails.DoesNotExist:
            return Response({'message': 'Server details not found'}, status=status.HTTP_404_NOT_FOUND)
        except ServerType.DoesNotExist:
            return Response({'message': 'Server type not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            qr = ''
            # q_id = dashboard_data.objects.get(id=dashboard_id,user_id = user_id)
            # query_id = q_id.queryset_id
            joining= QuerySets.objects.get(queryset_id = query_id,user_id = user_id)
            query_set = joining.custom_query
            if DataSource_querysets.objects.filter(queryset_id = query_id,user_id = user_id).exists():
                datasource_id = DataSource_querysets.objects.get(queryset_id = query_id,user_id = user_id)
                datasource_query = datasource_id.custom_query
                qr += datasource_query
            else:
                qr += query_set
            if datatype in ["TIME","DATETIME","YEAR","TIMESTAMP","TIMESTAMPTZ","DATE","NUMERIC"]:
                col1 =date_format_syntaxes[dtype](column)
                col_query = "SELECT DISTINCT {} FROM ({})temp".format(col1,qr)
            else:
                col_query = "SELECT DISTINCT {} FROM ({})temp".format(quotes[dtype][0]+column+quotes[dtype][1],qr)
            col_query = convert_query(col_query,dtype)
          
            if dtype.lower() == "microsoftsqlserver":
                data = cursor.execute(str(col_query))
            elif dtype.lower() == "snowflake":
                col_query = col_query.replace('"', '')
                data = cursor.execute(text(col_query))
            else:
                data = cursor.execute(text(col_query))
            col = data.fetchall()
            col_data = [j for i in col for j in i]
            for i in col:
                for j in i:
                    d1 = j
                    col_data.append(d1)
            
            if search_term:
                col_data = [item for item in col_data if search_term.lower() in str(item).lower()]
            
            col_data = list(set(col_data))

            return Response({"col_data":col_data,"column_name":column}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND) 

        



        
class FinalDashboardFilterData(CreateAPIView):
    serializer_class = serializers.SheetDataSerializer

    def post(self, request, token):
        if token==settings.DEFAULT_TOKEN:
            tok_status=200
        else:
            tok1 = test_token(token)
            tok_status=tok1['status']
        if tok_status != 200:
            return Response({"message": tok1['message']}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'serializer error'}, status=status.HTTP_204_NO_CONTENT)

        filter_ids = serializer.validated_data["id"]
        input_lists = serializer.validated_data["input_list"]

        if len(filter_ids) != len(input_lists):
            return Response({'message': 'Filter IDs and input lists count mismatch'}, status=status.HTTP_400_BAD_REQUEST)

        filter_ids = [fid for fid, il in zip(filter_ids, input_lists) if il]
        input_lists = [il for il in input_lists if il]

        if not filter_ids or not input_lists:
            return Response({'message': 'No valid filters provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            query_id = DashboardFilters.objects.get(id = filter_ids[0]).queryset_id
            dashboard_id = DashboardFilters.objects.get(id=filter_ids[0]).dashboard_id
            database_id,file_id,joining_tables,custom = get_server_id(query_id)
        except DashboardFilters.DoesNotExist:
            return Response({'message': 'Invalid filter ID'}, status=status.HTTP_404_NOT_FOUND)
        except dashboard_data.DoesNotExist:
            return Response({'message': 'Invalid dashboard ID'}, status=status.HTTP_404_NOT_FOUND)

        if token==settings.DEFAULT_TOKEN:
            dashboarddata=dashboard_data.objects.get(id=dashboard_id)
            user_id=dashboarddata.user_id
        else:
            user_id = tok1['user_id']

        try:
            con_data =connection_data_retrieve(database_id,file_id,user_id)
            if con_data['status'] ==200:                
                ServerType1 = con_data['serverType1']
                server_details = con_data['server_details']
                file_type = con_data["file_type"]
                file_data =con_data["file_data"]
                dtype = con_data['dbtype']
            else:
                return Response({'message':con_data['message']},status = status.HTTP_404_NOT_FOUND)
            serdt=server_details_check(ServerType1,server_details,file_type,file_data,eval(joining_tables),custom)
            if serdt['status']==200:
                engine=serdt['engine']
                cursor=serdt['cursor']
            else:
                return Response({'message':serdt['message']},status=serdt['status'])
        except ServerDetails.DoesNotExist:
            return Response({'message': 'Server details not found'}, status=status.HTTP_404_NOT_FOUND)
        except ServerType.DoesNotExist:
            return Response({'message': 'Server type not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            filter_details = []
            for filter_id in filter_ids:
                dash_filter = DashboardFilters.objects.get(id=filter_id)
                filter_details.append({
                    "filter_id": filter_id,
                    "dashboard_id": dash_filter.dashboard_id,
                    "sheet_list": eval(dash_filter.sheet_id_list),
                    "column_name": dash_filter.column_name,
                    "datatype": dash_filter.column_datatype
                })
                
            sheet_ids = set()
            for filter_detail in filter_details:
                sheet_ids.update(filter_detail['sheet_list'])
            sheet_ids = list(sheet_ids)

            sheet_details = get_sheet_details(sheet_ids, user_id)
            sheet_mapping = {item["sheetfilter_queryset_id"]: item["sheet_id"] for item in sheet_details}
            sheetfilter_queryset_ids = [item["sheetfilter_queryset_id"] for item in sheet_details]

            details = []
            for sfid in sheetfilter_queryset_ids:
                try:
                    queryset_obj = SheetFilter_querysets.objects.get(Sheetqueryset_id=sfid)
                    sheet_id = sheet_mapping.get(sfid)
                    details.append({
                        "sheet_id": sheet_id,
                        "Sheetqueryset_id": queryset_obj.Sheetqueryset_id,
                        "query_id":queryset_obj.queryset_id,
                        "custom_query": queryset_obj.custom_query,
                        "columns": queryset_obj.columns,
                        "rows": queryset_obj.rows
                    })
                except Exception as e:
                    return Response(f'{e}', status=status.HTTP_404_NOT_FOUND)

            sql_queries = []
            for detail in details:
                custom_query = detail.get("custom_query", "")
                sheetq_id = detail["Sheetqueryset_id"]
                sheet1_id = detail["sheet_id"]
               
                where_clauses = []
                for i, filter_detail in enumerate(filter_details):
                    if sheet1_id in filter_detail["sheet_list"]:
                        column = filter_detail["column_name"]
                        input_list = input_lists[i]
                        if filter_detail["datatype"] == "TIMESTAMPTZ" or filter_detail["datatype"] == 'TIMESTAMP'or filter_detail["datatype"] == 'DATE' :
                            f = transform_list(input_list)
                            formatted_list = tuple(f)
                            input1 = str(formatted_list).replace(',)', ')')
                            where_clauses.append(f"TO_CHAR(\"{column}\", 'YYYY-MM-DD') IN {input1}")
                        else:
                            try:
                                formatted_list = tuple(int(item) for item in input_list)
                            except ValueError:
                                f = transform_list(input_list)
                                formatted_list = tuple(f)
                            input1 = str(formatted_list).replace(',)', ')')
                            where_clauses.append(f'"{column}" IN {input1}')
                final_query = custom_query.strip()
                if 'GROUP BY' in final_query.upper():
                    parts = re.split(r'(\sGROUP\sBY\s)', final_query, flags=re.IGNORECASE)
                    main_query = parts[0]
                    group_by_clause = parts[1] + parts[2]
                else:
                    main_query = final_query
                    group_by_clause = ''

                if 'WHERE' in main_query.upper():
                    main_query += " AND " + " AND ".join(where_clauses)
                else:
                    main_query += " WHERE " + " AND ".join(where_clauses)

                final_query = main_query + " " + group_by_clause

                try:
                    final_query = convert_query(final_query, dtype.lower())
                    colu = cursor.execute(text(final_query))
                    if dtype.lower() == "microsoftsqlserver":
                        colu = cursor.execute(str(final_query))
                        col_list = [column[0].replace(":OK",'') for column in cursor.description]
                    elif dtype.lower() == "snowflake":
                        colu = cursor.execute(text(final_query))
                        col_list = [column.replace(":OK",'') for column in colu.keys()]
                    else:
                        colu = cursor.execute(text(final_query))
                        col_list = [column.replace(":OK",'') for column in colu.keys()]
                    col_data = []
                    
                    for row in colu.fetchall():
                        col_data.append(list(row))
                    
                    a11 = []
                    rows11=[]
                    kk=ast.literal_eval(detail['columns'])
                    
                    for i in kk:
                        result = {}
                        
                        a = i.replace(' ','')
                        a = a.replace('"',"")
                        
                        if a in col_list:
                            ind = col_list.index(a)

                            result['column'] = col_list[ind]
                            result['result'] = [item[ind] for item in col_data] 
                        a11.append(result)

                    
                    for i in ast.literal_eval(detail['rows']):
                        result1={}
                        a = i.replace(' ','')
                        a =a.replace('"',"") 
                        if a in col_list:
                            ind = col_list.index(a)
                            result1['column'] = col_list[ind]
                            result1['result'] = [item[ind] for item in col_data]
                        rows11.append(result1)
                    
                    sheet_id11 = sheet_data.objects.get(id = sheet1_id,sheet_filt_id = sheetq_id)
                    sql_queries.append({
                        "sheet_id": sheet1_id,
                        "Sheetqueryset_id": sheetq_id,
                        "final_query": final_query,
                        "columns": a11,
                        "rows": rows11,
                        "queryset_id": query_id,
                        "chart_id":sheet_id11.chart_id
                    })
                except Exception as e:
                    # print(e)
                    return Response({'message': "Invalid Input Data for Column"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            return Response(sql_queries, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
                   

        

        
class Dashboard_filters_list(CreateAPIView):
    serializer_class = serializers.dashboard_filter_list

    def post(self, request, token):
        if token==settings.DEFAULT_TOKEN:
            tok_status=200
        else:
            role_list = roles.get_previlage_id(previlage=[previlages.view_dashboard_filter,previlages.view_dashboard,previlages.edit_dasboard])
            tok1 = roles.role_status(token, role_list)
            tok_status=tok1['status']

        if tok_status != 200:
            return Response({"message": tok1['message']}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'serializer error'}, status=status.HTTP_204_NO_CONTENT)

        dashboard_id = serializer.validated_data["dashboard_id"]
        try:
            dashboard_sheets = eval(dashboard_data.objects.get(id=dashboard_id).sheet_ids)
        except :
            return Response([], status=status.HTTP_200_OK)

        data = []
        if DashboardFilters.objects.filter(dashboard_id=dashboard_id).exists():
            dash_filter = DashboardFilters.objects.filter(dashboard_id=dashboard_id)
            for i in dash_filter:
                data.append({
                    "dashboard_filter_id": i.id,
                    "dashboard_id": i.dashboard_id,
                    "filter_name": i.filter_name,
                    "selected_column": i.column_name,
                    "sheets": i.sheet_id_list,
                    "datatype": i.column_datatype
                })

            for filter_data in data:
                sheet_ids = eval(filter_data["sheets"])  # Convert string representation of list to actual list
                filter_data["sheet_counts"] = {}

                for sheet_id in dashboard_sheets:
                    count = sheet_ids.count(sheet_id)
                    filter_data["sheet_counts"][sheet_id] = count

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response([],status=status.HTTP_200_OK)



class DashboardFilterDetail(CreateAPIView):
    serializer_class = serializers.dashboard_filter_applied

    def post(self, request, token):
        tok1 = test_token(token)
        if tok1['status'] != 200:
            return Response({"message": tok1['message']}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        filter_id = serializer.validated_data["filter_id"]
       
        if not DashboardFilters.objects.filter(id=filter_id).exists():
            return Response({"message": "Dashboard filter not found"}, status=status.HTTP_404_NOT_FOUND)
        
        dash_filter = DashboardFilters.objects.get(id=filter_id)
        query_id = DashboardFilters.objects.get(id = filter_id).queryset_id
        queryname = QuerySets.objects.get(queryset_id = query_id).query_name
        dash_id = dash_filter.dashboard_id
        dashboard = eval(dashboard_data.objects.get(id=dash_id).sheet_ids)
        all_sheet_ids = dashboard
        #Filter sheet_ids that match with query_id
        # sheet_id_d=[]
        # aaa = sheet_data.objects.filter(queryset_id=query_id)
        # for i in aaa:
        #     sheet_id_d.append(i.id)            
        dash_sheets = [
            sheet_id for sheet_id in all_sheet_ids
            if sheet_data.objects.filter(id=sheet_id, queryset_id=query_id).exists()
        ]
        dash_filter.sheet_id_list = eval(dash_filter.sheet_id_list)
        sheets_data = []
        for sheet_id in dash_sheets:
            sheet_name = sheet_data.objects.get(id=sheet_id).sheet_name
            sheets_data.append({
                "sheet_id": sheet_id,
                "sheet_name": sheet_name,
                "selected": sheet_id in dash_filter.sheet_id_list
            })
        
        data = {
            "dashboard_filter_id": dash_filter.id,
            "dashboard_id": dash_filter.dashboard_id,
            "filter_name": dash_filter.filter_name,
            "selected_column": dash_filter.column_name,
            "sheets": sheets_data,
            "queryname": queryname,
            "query_id": query_id,
            "datatype": dash_filter.column_datatype
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
class Nofiltersheet(CreateAPIView):
    serializer_class = serializers.dashboard_nosheet_data

    def post(self, request, token):
        tok1 = test_token(token)
        if tok1['status'] != 200:
            return Response({"message": tok1['message']}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        dashboard_id = serializer.validated_data["dashboard_id"]
        del_sheet_ids = serializer.validated_data["sheet_ids"]
        saved_sheets = del_sheet_ids
        
        filter_sheets = []
        filter_ids = DashboardFilters.objects.filter(dashboard_id=dashboard_id)
        sheet_ids = []

        for filter_obj in filter_ids:
            sheet_ids.extend(ast.literal_eval(filter_obj.sheet_id_list))
        
        
        remaining_sheets = [sheet for sheet in saved_sheets if sheet not in sheet_ids]
        sql_queries = []

        for s_id in remaining_sheets:
            sheet_details = sheet_data.objects.get(id=s_id)
            sheet_query_id = int(sheet_details.sheet_filt_id)

            try:
                # Fetching server details
                sheetfilter = SheetFilter_querysets.objects.get(Sheetqueryset_id=sheet_query_id)
                query_id = sheet_details.queryset_id
                database_id, file_id, joining_tables, custom = get_server_id(int(query_id))
                user_id = tok1['user_id']

                con_data = connection_data_retrieve(database_id, file_id, user_id)
                if con_data['status'] != 200:
                    return Response({'message': con_data['message']}, status=status.HTTP_404_NOT_FOUND)

                ServerType1 = con_data['serverType1']
                server_details = con_data['server_details']
                file_type = con_data["file_type"]
                file_data = con_data["file_data"]
                dtype = con_data['dbtype']

                serdt = server_details_check(ServerType1, server_details, file_type, file_data, eval(joining_tables), custom)
                if serdt['status'] != 200:
                    return Response({'message': serdt['message']}, status=serdt['status'])

                engine = serdt['engine']
                cursor = serdt['cursor']

                final_query = sheetfilter.custom_query
                final_query = convert_query(final_query, dtype.lower())

                if dtype.lower() == "microsoftsqlserver":
                    data = cursor.execute(str(final_query))
                else:
                    # final_query = final_query.replace('"', '') if dtype.lower() == "snowflake" else final_query
                    data = cursor.execute(text(final_query))

                col_list = [column.replace(":OK",'') for column in data.keys()]
                col_data = [list(row) for row in data.fetchall()]

                # Processing columns and rows
                columns_data = []
                rows_data = []

                for col_name in ast.literal_eval(sheetfilter.columns):
                    clean_col_name = col_name.replace(' ', '').replace('"', '')
                    if clean_col_name in col_list:
                        ind = col_list.index(clean_col_name)
                        columns_data.append({
                            "column": col_list[ind],
                            "result": [item[ind] for item in col_data]
                        })

                for row_name in ast.literal_eval(sheetfilter.rows):
                    clean_row_name = row_name.replace(' ', '').replace('"', '')
                    if clean_row_name in col_list:
                        ind = col_list.index(clean_row_name)
                        rows_data.append({
                            "column": col_list[ind],
                            "result": [item[ind] for item in col_data]
                        })

                sql_queries.append({
                    "sheet_id": s_id,
                    "Sheetqueryset_id": sheet_query_id,
                    "final_query": final_query,
                    "columns": columns_data,
                    "rows": rows_data,
                    "queryset_id": query_id,
                    "chart_id": sheet_details.chart_id
                })

            except (ServerDetails.DoesNotExist, ServerType.DoesNotExist):
                return Response({'message': 'Server details or server type not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"sql_queries": sql_queries}, status=status.HTTP_200_OK)


    

    
class DashboardFilterDelete(CreateAPIView):
    def delete(self, request, token,filter_id):
        role_list=roles.get_previlage_id(previlage=[previlages.delete_dashboard_filter])
        tok1 = roles.role_status(token,role_list)
        if tok1['status'] != 200:
            return Response({"message": tok1['message']}, status=status.HTTP_404_NOT_FOUND)
        sheet_ids = eval(DashboardFilters.objects.get(id = filter_id).sheet_id_list)

        if DashboardFilters.objects.filter(id=filter_id).exists():
            DashboardFilters.objects.get(id=filter_id).delete()
            return Response({"message": "Filter Deleted Successfully","sheet_ids":sheet_ids})
        else:
            return Response({"message": "Dashboard filter ID not found"}, status=status.HTTP_404_NOT_FOUND)
   


###########################################################################  api functions ###########################################################

def transform_list(data):
    transformed_data = []
    for element in data:
        if isinstance(element, list):
            if len(element) == 1 and isinstance(element[0], str) and ',' in element[0]:
                transformed_element = element[0]
            else:
                transformed_element = "'" + "','".join(element) + "'"
        else:
            transformed_element = element
        
        transformed_data.append(transformed_element)

    return transformed_data

def get_sheet_details(sheet_ids, user_id):
    details = []

    for sheet_id in sheet_ids:
        try:
            sheet_data_obj = sheet_data.objects.get(id=sheet_id, user_id=user_id)
            sheetfilter_queryset_id = sheet_data_obj.sheet_filt_id
            chart_id = sheet_data_obj.chart_id
            sheet_data_source = sheet_data_obj.datasrc
            queryset_id = sheet_data_obj.queryset_id

            details.append({
                "sheet_id": sheet_id,
                "chart_id": chart_id,
                "sheetfilter_queryset_id": sheetfilter_queryset_id,
                "sheet_data_source": sheet_data_source,
                "queryset_id": queryset_id
            })
        except sheet_data.DoesNotExist:
            raise Exception(f"sheet_data with id {sheet_id} and user_id {user_id} does not exist.")

    return details

def convert_query(query,dtype):
 
    a = {'postgresql':'postgres','oracle':'oracle','mysql':'mysql','sqlite':'sqlite','microsoftsqlserver':'tsql','snowflake':'snowflake'}
    if a[dtype]:
        res = a[dtype]

    else:
        res = 'invalid datatype'
    try:
        parsed_query = sqlglot.parse_one(query,read=res)
        converted_query = parsed_query.sql(dialect=res)
    except Exception as e:
        print(str(e),"YYYYYYYYYYYYY")
    

    return converted_query

def get_server_id(query_id):
    try:
        q_id = QuerySets.objects.get(queryset_id=query_id)
        # server_id = eval(q_id.server_id)
        # file_id = eval(q_id.file_id)
        # joining_tables = eval(q_id.table_names)
        # print(q_id.server_id,q_id.file_id,q_id.table_names,q_id.is_custom_sql)
        return q_id.server_id,q_id.file_id,q_id.table_names,q_id.is_custom_sql
        
    except dashboard_data.DoesNotExist:
        return None

def get_columns_list(samp, server_type):

    postgres_type_code_to_name = {
        16: 'BOOLEAN',
        20: 'BIGINT',
        23: 'INTEGER',
        1042: 'CHAR',
        1043: 'VARCHAR',
        1082: 'DATE',
        1114: 'TIMESTAMP',
        1184: 'TIMESTAMPTZ',
        1700: 'NUMERIC',
        2003: 'DECIMAL',
    }

    mysql_type_code_to_name = {
        0: 'DECIMAL',
        1: 'TINY',
        2: 'SHORT',
        3: 'LONG',
        4: 'FLOAT',
        5: 'DOUBLE',
        6: 'NULL',
        7: 'TIMESTAMP',
        8: 'LONGLONG',
        9: 'INT24',
        10: 'DATE',
        11: 'TIME',
        12: 'DATETIME',
        13: 'YEAR',
        14: 'NEWDATE',
        15: 'VARCHAR',
        16: 'BIT',
        245: 'JSON',
        246: 'NEWDECIMAL',
        247: 'ENUM',
        248: 'SET',
        249: 'TINY_BLOB',
        250: 'MEDIUM_BLOB',
        251: 'LONG_BLOB',
        252: 'BLOB',
        253: 'VAR_STRING',
        254: 'STRING',
        255: 'GEOMETRY'
    }

    sqlite_type_code_to_name = {
        'INTEGER': 'INTEGER',
        'TEXT': 'TEXT',
        'BLOB': 'BLOB',
        'REAL': 'REAL',
        'NUMERIC': 'NUMERIC',
    }

    snow_type_code_to_name = {
       
        
    }

    if server_type.upper() == 'POSTGRESQL':
        return postgres_type_code_to_name
    elif server_type.upper() == 'MYSQL':
        return mysql_type_code_to_name
    elif server_type.upper() == 'SQLITE':
        return sqlite_type_code_to_name
    elif server_type.upper() == 'SNOWFLAKE':
        return snow_type_code_to_name
    else:
        type_code_to_name = {}

  


class SearchSheetAndQuerySetList(CreateAPIView):
    serializer_class = serializers.test_data

    def post(self, request, token):
        tok1 = test_token(token)
        if tok1['status'] != 200:
            return Response({"message": tok1['message']}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        search_query = serializer.validated_data["search"]
        response_data = []

        try:
            sheet_data_queryset = sheet_data.objects.filter(sheet_name__icontains=search_query)
            queryset_data_queryset = QuerySets.objects.filter(query_name__icontains=search_query)

            for queryset in queryset_data_queryset:
                sheets = sheet_data.objects.filter(queryset_id=queryset.queryset_id)
                sheets_info = [
                    {"sheet_name": sheet.sheet_name, "sheet_id": sheet.id} for sheet in sheets
                ]
                
                response_data.append({
                    "queryset_name": queryset.query_name,
                    "queryset_id": queryset.queryset_id,
                    "sheet_data": sheets_info
                })

            for sheet in sheet_data_queryset:
                if not any(item['queryset_id'] == sheet.queryset_id for item in response_data):
                    queryset = QuerySets.objects.get(queryset_id=sheet.queryset_id)
                    sheets_info = [
                        {"sheet_name": sheet.sheet_name, "sheet_id": sheet.id}
                    ]
                    
                    response_data.append({
                        "queryset_name": queryset.query_name,
                        "queryset_id": queryset.queryset_id,
                        "sheet_data": sheets_info
                    })

            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


