from oauth2_provider.models import Application,AccessToken,RefreshToken
import datetime
from pytz import utc
from dashboard.models import *
from django.conf import settings
import requests
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from sqlalchemy import create_engine, inspect, MetaData, Table, text,insert
from sqlalchemy.exc import OperationalError
import json,os
import pandas as pd
from rest_framework import status
import pdfplumber
import plotly.graph_objects as go
from sqlalchemy.orm import sessionmaker
from .serializers import *
from django.db import transaction
from project import settings
from django.urls import reverse
from django.http import JsonResponse
from django.core.serializers import serialize as ss
from io import BytesIO
from rest_framework.decorators import api_view
import boto3
import calendar
import ast
import re
import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Float, Date, Time, DateTime, Numeric,TIMESTAMP,VARCHAR,BIGINT,SMALLINT,CHAR,Text,TEXT,VARBINARY
from .views import test_token
from collections import Counter
from django.views.decorators.csrf import csrf_exempt
import io
from dashboard.columns_extract import server_connection
from .Connections import file_save_1
from dashboard import roles,previlages
import sqlglot
from urllib.parse import quote
import numpy as np

integer_list=['numeric','int','float','number','double precision','smallint','integer','bigint','decimal','numeric','real','smallserial','serial','bigserial','binary_float','binary_double']
char_list=['varchar','bp char','text','varchar2','NVchar2','long','char','Nchar','character varying']
bool_list=['bool','boolean']
date_list=['date','time','datetime','timestamp','timestamp with time zone','timestamp without time zone','timezone','time zone','timestamptz'] 

def date_format(date_format1):
    date_func = {'year':'%Y','month':'%m','day':'%d','hour':'%H','minute':'%M','second':'%S','week numbers':'%W','weekdays':'%w','month/year':'%m/%Y','month/day/year':'%m/%d/%Y','count_distinct':'count_distinct'}
    return date_func.get(date_format1.lower(),'%Y-%m-%d')



def dtype_fun(dtype):
    a = {'postgresql':'postgres','oracle':'oracle','mysql':'mysql','sqlite':'sqlite','microsoftsqlserver':'tsql','snowflake':'snowflake'}
    if a[dtype]:
        res = a[dtype]
    else:
        res = 'invalid datatype'
    return res

def query_parsing(read_query,use_l,con_l): 
    use = dtype_fun(use_l)
    con = dtype_fun(con_l)
    use_q = sqlglot.parse_one(read_query,read=use)
    con_q = use_q.sql(con)
    return con_q


def map_dtype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return 'Int64'
    elif pd.api.types.is_float_dtype(dtype):
        return 'Float64'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'boolean'
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'datetime64[ns]'
    elif isinstance(dtype, np.dtype) and dtype.type == np.datetime64:  # Specific datetime64 handling
        return 'datetime64[ns]'
    elif isinstance(dtype, type(pd.Timestamp(0).date())):  # Handling datetime.date
        return 'date'
    else:
        return 'string'
    
def read_excel_file_data(file_path,filename,joining_tables,check):
    try:
        encoded_url = quote(file_path, safe=':/')
        xls = pd.ExcelFile(encoded_url)
        l=[]
        sheet_name = []
        url =f'sqlite:///local.db'
        engine = create_engine(url)
        tables = tables_get(joining_tables)
        if check==False:
            for i in xls.sheet_names:
                if i in tables:
                    data_csv = pd.read_excel(xls,sheet_name=i)
                    data_csv = data_csv.fillna(value='NA')
                    sheet_name.append(i)
                    for column in data_csv.columns:
                        non_null_data = data_csv[column]
                        if not non_null_data.empty:
                            dtype = non_null_data.dtype
                            mapped_dtype = map_dtype(dtype)
                            data_csv[column] = data_csv[column].astype(mapped_dtype)
                    # for column in data_csv.columns:
                    #     if data_csv[column].dtype == 'object':
                    #         data_csv[column] = data_csv[column].astype(str)  # Convert to TEXT
                    #     elif data_csv[column].dtype == 'int64':
                    #         data_csv[column] = data_csv[column].astype(int)  # Convert to INTEGER
                    #     elif data_csv[column].dtype == 'float64':
                    #         data_csv[column] = data_csv[column].astype(float)
                    data_csv.to_sql(i, engine, index=False, if_exists='replace')
                else:
                    pass
        else:
            for i in xls.sheet_names:
                data_csv = pd.read_excel(xls,sheet_name=i)
                data_csv = data_csv.fillna(value='NA')
                sheet_name.append(i)
                for column in data_csv.columns:
                    non_null_data = data_csv[column]
                    if not non_null_data.empty:
                        dtype = non_null_data.dtype
                        mapped_dtype = map_dtype(dtype)
                        data_csv[column] = data_csv[column].astype(mapped_dtype)
                # for column in data_csv.columns:
                #     if data_csv[column].dtype == 'object':
                #         data_csv[column] = data_csv[column].astype(str)  # Convert to TEXT
                #     elif data_csv[column].dtype == 'int64':
                #         data_csv[column] = data_csv[column].astype(int)  # Convert to INTEGER
                #     elif data_csv[column].dtype == 'float64':
                #         data_csv[column] = data_csv[column].astype(float)
                data_csv.to_sql(i, engine, index=False, if_exists='replace')
                
        f_dt = {
            "status":200,
            "engine":engine,
            "cursor":engine.connect(),
            "tables_names":sheet_name
        }
        return f_dt
    except Exception as e:
        f_dt = {
            "status":400,
            "message":e
        }
        return f_dt



def read_csv_file_data(file_path,filename,check):
    try:
        data_csv = pd.read_csv(file_path)
        data_csv = data_csv.fillna(value='NA')
        for column in data_csv.columns:
                non_null_data = data_csv[column]
                if not non_null_data.empty:
                    dtype = non_null_data.dtype
                    mapped_dtype = map_dtype(dtype)
                    data_csv[column] = data_csv[column].astype(mapped_dtype)

        url =f'sqlite:///local.db'
        engine = create_engine(url)
        data_csv.to_sql(filename, engine, index=False, if_exists='replace')
        f_dt = {
                "status":200,
                "engine":engine,
                "cursor":engine.connect(),
                "tables_names":[filename]
            }
        return f_dt
    except Exception as e:
        f_dt = {
            "status":400,
            "message":e
        }
        return f_dt

def server_details_check(ServerType1,server_details,file_type,file_data,joining_tables,check):
    if file_type is None or  file_data =='' or file_data is  None or file_data =='':
        server_conn=server_connection(server_details.username,server_details.password,server_details.database,server_details.hostname,server_details.port,server_details.service_name,ServerType1.server_type.upper(),server_details.database_path)
        if server_conn['status']==200:
            engine=server_conn['engine']
            cursor=server_conn['cursor']
            data = {
                'status':200,
                'engine':engine,
                'cursor':cursor,
                'tables':[]
            }
        else:
            data = {
                'status':server_conn['status'],
                'message':server_conn
            }
    elif file_type is not None or  file_data !='' or file_data is not  None or file_data !='':
        pattern = r'/insightapps/(.*)'
        match = re.search(pattern, str(file_data.source))

        filename = match.group(1)
        file12,fileext = filename.split('.')
        file = re.sub(r'^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', '', str(file12))
        file_url = file_data.source
        
        if (file_type.upper()=='EXCEL' and fileext == 'xlsx') or (file_type.upper()=='EXCEL' and fileext == 'xls'):
            read_data = read_excel_file_data(file_url,file,joining_tables,check)
        elif  file_type.upper()=='CSV' and fileext == 'csv':
            read_data = read_csv_file_data(file_url,file,check)
        else:
            return 'Nodata'

        if read_data['status'] ==200:
                data = {
                        'status':200,
                        'engine':read_data['engine'],
                        'cursor':read_data['cursor'],
                        'tables':read_data['tables_names']
                    } 
        else:
            data =read_data
    else:
        data = {
            'status':400,
            'message':'no Data'
        }
        # elif file_type.upper()=='PDF' and fileext == 'pdf':
        #     read_data = read_pdf_file(file_url,filename,file_data.id)
        # elif file_type.upper()=='TEXT' and fileext == 'txt':
        #     read_data = read_text_file(file_url,filename,file_data.id)
    return data

    

def relation(tables,table_col,dbtype):
    try:
        list_of_tables={}
        list_of_tables1={}
        for i in range(len(tables)):
            table1 = []
            table2 =[]
            for j in table_col:
                if tables[i] == j[0]:
                    table1.append(f'{j[1]}:{j[2]}')
                    table2.append(f'{j[1]}')
            list_of_tables[tables[i]] = table1 
            list_of_tables1[tables[i]] = table2
        dynamic_con = [] 
        comp = [i for i in range(1,len(tables))]
        relation_tables= []
        for i in range(0,len(tables)):
            for j in range(i+1,len(tables)):
                if i<j and j  in comp:
                    lisst = list_of_tables[tables[i]]
                    liset = list_of_tables[tables[j]]
                    dict1 = {item.split(':')[0]: item for item in lisst}
                    dict2 = {item.split(':')[0]: item for item in liset}
                    intersection_list = list(set(dict1.keys())& (set(dict2.keys()))) 
                    final_data =[]
                    for name in intersection_list:
                        if name in dict1:
                            final_data.append(dict1[name])
                        if name in dict2:
                            final_data.append(dict2[name])
                    if intersection_list:
                        jj = (tables[i],tables[j])
                        relation_tables.append(jj)
                        if j in comp:
                            comp.remove(j)
                            sorted_strings_list =  sorted(final_data, key=lambda x: x.split(':')[1].lower() not in integer_list)
                            aa= [s.split(':')[0] for s in sorted_strings_list]
                            formast = tables[i].split(' ')
                            formaet = tables[j].split(' ')
                            if dbtype.lower()=='snowflake':
                                string = [f'{formast[1]}.{aa[0]} = {formaet[1]}.{aa[0]}']
                            else:
                                string = [f'{formast[1]}.\"{aa[0]}\" = {formaet[1]}.\"{aa[0]}\"']
                            string = [query_parsing(string[0],'sqlite',dbtype)]
                            if len(dynamic_con)>j:
                                dynamic_con.append(string)
                            else:
                                dynamic_con.insert(j-1,string)
                        else:
                            pass
                    else:
                        pass
        response_data = {
                "status" : 200,
                "relation":relation_tables,
                "conditions":dynamic_con,
                "comp" : comp

        }
    except Exception as e:
         response_data = {
                "status" : 404,
                "message" : str(e)

        }
    return response_data

def building_query(self,tables,join_conditions,join_types,engine,dbtype):
    table_col= []
    alias_columns = []
    try:
        for schema,table_name,alias in tables:
            metadata = MetaData()
            if dbtype == 'microsoftsqlserver':
                qu =f"""
                    SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = '{table_name}'
                    AND TABLE_SCHEMA = '{schema}'
                """
                # pyodbc cursor get column names
                # columns = cursor.columns(table=table_name)

                # columns = [{'name':column.COLUMN_NAME,'col':str(column.DATA_TYPE)} for column in columns]
                cursor = engine.cursor()
                a1=cursor.execute(qu)
                columns = [{'name':column.COLUMN_NAME,'col':str(column.DATA_TYPE)} for column in a1.fetchall()]
            else:
                table = Table(table_name, metadata,autoload_with =engine,schema = schema)
                columns= [{'name':column.name,'col':str(column.type)} for column in table.columns]
            for column in columns:
                if dbtype.lower()=='snowflake':
                    a =r'{}.{} "{}"'.format(schema,table_name,alias)
                else:
                    a =r'"{}"."{}" "{}"'.format(schema,table_name,alias)
                alias_columns.append(f"\"{alias}\".\"{column['name']}\"")
                table_col.append((f'{a}',column['name'],column['col'].lower()))
    except Exception as e:
        return_data = {
            "status":400,
            "message" : f'{e}  table not present in databse'
        }
        return return_data
    if dbtype.lower()=='snowflake':
        tables = [r'{}.{} "{}"'.format(schema,table,alias) for schema,table,alias in tables]
    else:
        tables = [r'"{}"."{}" "{}"'.format(schema,table,alias) for schema,table,alias in tables]
    table_json = []
    for j in tables:
        for i in range(len(table_col)):
            if j==table_col[i][0]:
                json_str = {"table":table_col[i][0],"col":table_col[i][1],"dtype":table_col[i][2]}
                table_json.append(json_str)
    
    query = f"SELECT * FROM {tables[0]}"
    join_types1=[]
    
    try:
        length_condition_val = 0
        for i in join_conditions:
            if len(i)>0:
                length_condition_val+=1
            else:
                break
        if len(tables)-1==length_condition_val:
            
            try:
                for i in range(1, len(tables)):
                    if i-1 < len(join_types):
                        join_type = join_types[i-1]
                    else :
                        join_type = 'inner' 
                    join_types1.append(join_type)
                    query+=f" {join_type} JOIN {tables[i]}"
                    for index,user_cond in enumerate(join_conditions[i-1]):
                        if dbtype.lower()=='snowflake':
                            cond1,cond2 = user_cond.split('=')
                            one,two = cond1.split('.')
                            three,four = cond2.split('.')
                            cond1 = one+'.'+two.replace('"','')
                            cond2 = three+'.'+four.replace('"','')
                            user_cond = cond1+' = '+cond2
                            join_conditions[i-1][index] = user_cond
                        else:
                            
                            user_cond=user_cond
                        if index==0:
                            query += f"  ON {user_cond}"
                        else:
                             query += f"  AND {user_cond}"
            except Exception as e:
                error_data = {
                "status":400,
                "message" :str(e)
                }
                return error_data        
        else:
            get_data = relation(tables,table_col,dbtype)
            if get_data['status'] ==200:
                pass
            else:
                return {"message" : get_data['message']}
            comp = get_data['comp']
            relation_tables = get_data['relation']
            dynamic_cond = get_data['conditions']
            no_relation_tables =[]
            my_relation_tables=[]
            if comp:
                for i in comp:
                    if i>=len(join_conditions):
                        schema_table,table_name = tables[i].split(' ')
                        # schema,table = schema_table.split('.')
                        no_relation_tables.append(table_name)
                    else:
                        # index_in_tables = literal_eval(tables).index(i)
                        for user_cond in join_conditions:
                            try:
                                if len(user_cond)>=1:
                                    match = tables[i].split(' ')[1]
                                    cond1,cond2 = user_cond[0].replace("'",'').split('=')
                                    one,two = cond1.split('.')
                                    three,four = cond2.split('.')
                                    cond1 = one+'.'+two.replace('"','')
                                    cond2 = three+'.'+four.replace('"','')
                                    if match==one.strip() or match==three.strip():
                                        k=''
                                        one1=''
                                        three1=''
                                        for table in tables:
                                            if one in table:
                                                one1 += table
                                            elif three in table:
                                                three1 += table
                                            else:
                                                pass
                                        k=(one1,three1)
                                        relation_tables.insert(i-1,k)                                  
                                    # else:
                                    #     k=''
                                    #     one1=''
                                    #     three1=''
                                    #     for table in tables:
                                    #         if one in table:
                                    #             one1 += table
                                    #         elif three in table:
                                    #             three1 += table
                                    #         else:
                                    #             pass
                                    #     k=(one1,three1)
                                    #     print(k)
                                    #     relation_tables.insert(i-1,k)
                                else:
                                    pass
                            except Exception as e:
                                print(e)
                        
                    # bb = tables[i].split(' ')[1]
                    # print(i)
                    # for index,table in enumerate(literal_eval(tables)):
                    #     print(len(join_conditions),index)
                    #     if bb in table and index<len(join_conditions):
                    #         print(bb)
                    #         pass
                    #     else:
                    #         print('kk',bb)
                    #         print(index)
                    #         no_relation_tables.append(bb)
            else:
                pass
            if  no_relation_tables!=[] : 

                return_data = {
                    "status":204,   
                    "relation" : join_conditions,
                    "no_relation":no_relation_tables
                    }
                return return_data
            
            else:    
                my_relation_tables = relation_tables
                condition = {}
                # join_conditions.pop()
                # join_conditions.append(dynamic_cond[0])
                for i in range(len(my_relation_tables)):
                    ll1= []
                    if join_conditions[i]:
                        a = join_conditions[i]
                    else:
                        a = dynamic_cond[-1]
                        join_conditions[i].append(a[0])
                    ll1.append(a)
                    key = my_relation_tables[i]
                    condition[key] = ll1
                for i in range(0, len(tables)):
                    key_data = list(condition.keys())
                    compare_value = key_data[i-1]
                    for j in range(0,len(key_data)):
                        if (tables[i-1],tables[j+1]) in(condition):
                            if j < len(join_types):
                                join_type = join_types[j-1]
                            else :
                                join_type = 'inner' 
                            join_types1.append(join_type)
                            query+= f' {join_type} join {tables[j+1]}'
                            if len(condition[compare_value])>=1:
                                for index,cond in enumerate(condition[compare_value]):
                                    if index ==0:
                                        query+= f' on {cond[0]}'
                                    else:
                                        query+= f" and {cond[0]} " 
                                             
    except Exception as e:
        error_data = {

        "status":400,
        "message" :f'{e}'
            }
        return error_data
    return_data ={
    "status" :200,
    "query_data" : query,
    "joining" : join_conditions,
    "tables" :table_json,
    "join_types" : join_types1,
    "make_columns":alias_columns
        
    }
    return return_data


def connection_data_retrieve(server_id,file_id,user_id):
    if file_id is None or file_id =='':         
        try:
            server_details =ServerDetails.objects.get(user_id = user_id, id=server_id)

            ServerType1 = ServerType.objects.get(id = server_details.server_type)
            dbtype = ServerType1.server_type.lower()
            file_type =None
            file_data=None
            data = {
                "status":200,
                "server_details":server_details,
                "serverType1":ServerType1,
                "dbtype" : dbtype,
                "file_type":file_type,
                "file_data":file_data
                
           }
        except:
            data ={
                "status":400,
                "message":"Data Not Found"
            }
    else:
        try:
            file_data = FileDetails.objects.get(user_id = user_id,id = file_id)
            file_type = FileType.objects.get(id = file_data.file_type).file_type
            dbtype = 'sqlite'
            ServerType1 =None
            server_details=None
            data = {
                "status":200,
                "server_details":server_details,
                "serverType1":ServerType1,
                "dbtype" : dbtype,
                "file_type":file_type,
                "file_data":file_data
                
            }
        except Exception as e:
                data ={
                "status":400,
                "message":"Data Not Found"
            }
    return data


def tables_get(joining_tables):
    tables=[]
    for i in joining_tables:
        tables.append(i[1])
    return tables

class rdbmsjoins(CreateAPIView):
    serializer_class = tablejoinserializer
    @transaction.atomic
    @csrf_exempt
    def post(self,request,token):
        tok1 = test_token(token)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            user_id = tok1['user_id']
            if serializer.is_valid(raise_exception=True):
                server_id = serializer.validated_data['database_id']
                query_set_id = serializer.validated_data['query_set_id']
                joining_tables = serializer.validated_data['joining_tables']
                join_type = serializer.validated_data['join_type']
                join_table_conditions= serializer.validated_data['joining_conditions']
                dragged_array = serializer.validated_data['dragged_array']
                # query_name = serializer.validated_data['query_name']
                file_id = serializer.validated_data['file_id']
            else:
                return Response({'message':'serializer error'},status=status.HTTP_204_NO_CONTENT) 
            con_data =connection_data_retrieve(server_id,file_id,user_id)
            if con_data['status'] ==200:                
                ServerType1 = con_data['serverType1']
                server_details = con_data['server_details']
                file_type = con_data["file_type"]
                file_data =con_data["file_data"]
                dbtype = con_data['dbtype']
            else:
                return Response({'message':con_data['message']},status = status.HTTP_404_NOT_FOUND)
            serdt=server_details_check(ServerType1,server_details,file_type,file_data,joining_tables,False)
            if serdt['status']==200:
                engine=serdt['engine']
                cur=serdt['cursor']
            else:
                return Response({'message':serdt['message']},status=serdt['status'])
            
            if len(joining_tables) ==0:
                Response_data= {
                        "query_set_id" : 0,
                        "relation_btw_tables": [],
                        'joining_condition': [],
                        'tables_col' :[],
                        "join_types": [],
                        "joining_condition_list" : []
                                }
                QuerySets.objects.filter(queryset_id = query_set_id).delete()
                return JsonResponse({"message":"Joining tables successfully","table_columns_and_rows":Response_data},status=status.HTTP_200_OK,safe=False)
            else:
                for index,i in enumerate(join_table_conditions):
                    for index1,j in enumerate(i):
                        if j:
                            new_cond = query_parsing(j,'sqlite',dbtype)
                            join_table_conditions[index][index1] = new_cond
                        else:
                            pass
                if file_id is not None and file_id !='':
                    for i in joining_tables:
                        i[0] ='main'
                responce = building_query(self,joining_tables,join_table_conditions,join_type,engine,dbtype)
                try:
                    if responce['status']==200:
                        query1 = responce['query_data']                        
                    elif responce["status"] ==400:
                        return Response({'message':responce["message"]},status=status.HTTP_400_BAD_REQUEST)
                    elif responce["status"]==204:
                        return Response({'message':f'No Relation Found {responce["no_relation"]}','joining_condition' :responce['relation']},status=status.HTTP_404_NOT_FOUND)
                    else:
                        pass
                    aa = alias_to_joins(responce['make_columns'],dbtype)

                    column_list11 = ','.join(aa)
                    
                    query1 = query1.replace('*',column_list11)
                    converted_query = query_parsing(query1,'sqlite',dbtype)
                    # if dbtype=="microsoftsqlserver":
                    #     query="{}".format(converted_query)
                    #     rows = cur.execute(query)
                    # # elif dbtype.lower()=='snowflake':
                    # #     # converted_query = converted_query.replace('"','')
                    # #     rows = cur.execute(text(converted_query))
                    # else:
                    #     rows = cur.execute(text(converted_query))
                        
                    # table_data = rows.fetchall()
                    if server_id is None or server_id =='':
                        query_set_id = query_set_id if query_set_id else 0
                        file_path = file_save_1(dragged_array,file_id,query_set_id,'datasource',"")
                    else:
                        query_set_id = query_set_id if query_set_id else 0
                        file_path = file_save_1(dragged_array,server_id,query_set_id,'datasource',"")

                    # col_data =[]   
                    # for i in table_data:
                    #     d1 = list(i)
                    #     col_data.append(d1)
                    if query_set_id is None or query_set_id==0:
                        a = QuerySets.objects.create(
                            user_id = user_id,
                            server_id = server_id ,
                            file_id = file_id,
                            table_names = joining_tables,
                            join_type = responce['join_types'],
                            joining_conditions  = responce['joining'],
                            custom_query = converted_query,
                            datasource_path = file_path['file_key'],
                            datasource_json = file_path['file_url'],
                            # query_name = query_name
                            
                        )
                        id = a.queryset_id
                    else:
                        a = QuerySets.objects.filter(queryset_id = query_set_id).update(
                            user_id = user_id,
                            server_id = server_id,
                            file_id = file_id,
                            table_names = joining_tables,
                            join_type = responce['join_types'],
                            joining_conditions  = responce['joining'],
                            custom_query = converted_query,
                            datasource_path = file_path['file_key'],
                            datasource_json = file_path['file_url'],
                            updated_at =datetime.datetime.now(),
                            # query_name = query_name
                            
                        )
                        id = query_set_id
                    joining_condition_list=[]
                    for i in responce['joining']:   
                        for j in i:
                            list_map = [j]
                            joining_condition_list.append(list_map)
                    Response_data= {
                        "file_id":file_id,
                        "database_id":server_id,
                        "query_set_id" : id,
                        # "query_name":query_name,
                        'joining_condition': responce['joining'],
                        'tables_col' :responce['tables'],
                        "join_types": responce['join_types'],
                        "joining_condition_list" : joining_condition_list
                                }
                except Exception as e:
                    return Response({"message":f'{e}'},status=status.HTTP_400_BAD_REQUEST)
            if file_id is not None and file_id !='':
                delete_tables_sqlite(cur,engine,serdt['tables'])   
                cur.close()
                engine.dispose()
            else:
                cur.close()
                # engine.dispose()
            return JsonResponse({"message":"Joining tables successfully","table_columns_and_rows":Response_data},status=status.HTTP_200_OK,safe=False)
        else:
            return Response({"message":tok1['message']},status=status.HTTP_404_NOT_FOUND)
      
def delete_tables_sqlite(cur,engine,tables):
    # try:
    #     if len(tables)>0:
    #         print(tables)
    #         for table1 in tables:
    #             drop_table_sql = f'DROP TABLE IF EXISTS \"{table1}\";'
    #             a= cur.execute(text(drop_table_sql))
    #         cur.commit()
    #         print(a)
    # except Exception as e:
        # print(e)
    try:
        with cur as connection:
            if len(tables) > 0:
                for table in tables:
                    drop_table_sql = text(f'DROP TABLE IF EXISTS \"{table}\";')
                    connection.execute(drop_table_sql)
            connection.commit()
    except Exception as e:
        print(e)
            # engine.commit()

# class joining_query_data(CreateAPIView):
#     serializer_class = queryserializer
#     @transaction.atomic
#     def post(self,request,token):
#         tok1 = test_token(token)
#         if tok1['status']==200:
#             serializer = self.serializer_class(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 server_id = serializer.validated_data['database_id']
#                 file_id = serializer.validated_data['file_id']
#                 query_id= serializer.validated_data['query_id']
#                 row_limit = serializer.validated_data['row_limit']
#                 datasource_queryset_id  = serializer.validated_data['datasource_queryset_id']

#             else:
#                 return Response({'message':'serializer error'},status=status.HTTP_204_NO_CONTENT)
#             user_id = tok1['user_id']
#             if query_id == '0':
#                 data={
#                 "column_data" : [],
#                 'row_data' : [],
#                 "query_exection_time":0.00,
#                 "no_of_rows":0,
#                 "no_of_columns":0
#                 }
#                 return Response(data,status=status.HTTP_200_OK) 
#             else:
#                 con_data =connection_data_retrieve(server_id,file_id,user_id)
#                 if con_data['status'] ==200:                
#                     ServerType1 = con_data['serverType1']
#                     server_details = con_data['server_details']
#                     file_type = con_data["file_type"]
#                     file_data =con_data["file_data"]
#                     dbtype = con_data['dbtype']
#                 else:
#                     return Response({'message':con_data['message']},status = status.HTTP_404_NOT_FOUND)
#                 try:
#                     if datasource_queryset_id is None:
#                         query_data = QuerySets.objects.get(queryset_id = query_id,user_id = user_id)
#                         query_name=query_data.query_name
#                     else:
#                         query_data = DataSource_querysets.objects.get(datasource_querysetid = datasource_queryset_id,user_id = user_id,queryset_id = query_id)
#                         query_data1 = QuerySets.objects.get(queryset_id = query_id,user_id = user_id)
#                         query_name=query_data1.query_name
#                 except:
#                     return Response({'message':'Data not found'},status=status.HTTP_400_BAD_REQUEST)
#                 query_data2 = QuerySets.objects.get(queryset_id = query_id,user_id = user_id)
#                 serdt=server_details_check(ServerType1,server_details,file_type,file_data,literal_eval(query_data2.table_names),query_data2.is_custom_sql)                
#                 if serdt['status']==200:
#                     engine=serdt['engine']
#                     cur=serdt['cursor']
#                 else:
#                     return Response({'message':serdt['message']},status=serdt['status'])
#                 st=datetime.datetime.now(utc)
#                 if dbtype.lower()=="microsoftsqlserver":
#                     query="{}".format(query_data.custom_query)
#                     result_proxy = cur.execute(query)
#                     result_column_values = cur.description
#                 else:
#                     result_proxy = cur.execute(text(query_data.custom_query))
#                     # query = query_data.custom_query + f'limit {row_limit}'
#                     # actual_query = query_parsing(query,dbtype,dbtype)
#                     # result_proxy = cur.execute(text(actual_query))
#                     result_column_values = result_proxy.cursor.description               
#                 results = result_proxy.fetchall()
#                 temp_class = Sqlite3_temp_table(query_data.custom_query,dbtype)
#                 table_created = temp_class.create(result_column_values,results,f'join_query{user_id}')
#                 query_string = f'select * from join_query{user_id} limit {row_limit}'
#                 qr_tl=f'select * from join_query{user_id}'
#                 query_result = temp_class.query(query_string)        
#                 qr_rest = temp_class.query(qr_tl)         
#                 if query_result['status'] ==200:
#                     result = query_result['result_data']
#                     rl_count = qr_rest['result_data']
#                     # st = query_result['st']
#                     # et = query_result['et']
#                 else:
#                     return Response({'message':query_result['message']},status = status.HTTP_400_BAD_REQUEST)
#                 et=datetime.datetime.now(utc)
#                 column_names = query_result['columns']
#                 column_list = [column for column in column_names]
#                 data = [list(row) for row in result]
#                 data1 = [list(row) for row in rl_count]
#                 data={
#                     "database_id":server_id,
#                     "file_id":file_id,
#                     "query_set_id" : query_data.queryset_id, 
#                     "queryset_name":query_name,
#                     "custom_query" : query_data.custom_query,
#                     "column_data" : column_list,
#                     'row_data' : data,
#                     "is_custom_query":query_data.is_custom_sql,
#                     "query_exection_time":et-st,
#                     "total_rows":len(data1),
#                     "no_of_rows":len(data),
#                     "no_of_columns":len(column_list),
#                     "created_at":query_data.created_at,
#                     "updated_at":query_data.updated_at,
#                     "query_exection_st":st.time(),
#                     "query_exection_et":et.time()
#                 }
#                 temp_class.delete(f'join_query{user_id}')
#                 if file_id is not None and file_id !='':
#                     delete_tables_sqlite(cur,engine,serdt['tables'])   
#                     cur.close()
#                     engine.dispose()
#                 else:
#                     cur.close()
#                     #  engine.dispose()      
#                 return Response(data,status=status.HTTP_200_OK)
#         else:
#             return Response({"message":tok1['message']},status=status.HTTP_404_NOT_FOUND)
        

class joining_query_data(CreateAPIView):
    serializer_class = queryserializer
    @transaction.atomic
    def post(self,request,token):
        tok1 = test_token(token)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                server_id = serializer.validated_data['database_id']
                file_id = serializer.validated_data['file_id']
                query_id= serializer.validated_data['query_id']
                row_limit = serializer.validated_data['row_limit']
                datasource_queryset_id  = serializer.validated_data['datasource_queryset_id']

            else:
                return Response({'message':'serializer error'},status=status.HTTP_204_NO_CONTENT)
            user_id = tok1['user_id']
            if query_id == '0':
                data={
                "column_data" : [],
                'row_data' : [],
                "query_exection_time":0.00,
                "no_of_rows":0,
                "no_of_columns":0
                }
                return Response(data,status=status.HTTP_200_OK) 
            else:
                con_data =connection_data_retrieve(server_id,file_id,user_id)
                if con_data['status'] ==200:                
                    ServerType1 = con_data['serverType1']
                    server_details = con_data['server_details']
                    file_type = con_data["file_type"]
                    file_data =con_data["file_data"]
                    dbtype = con_data['dbtype']
                else:
                    return Response({'message':con_data['message']},status = status.HTTP_404_NOT_FOUND)
                try:
                    if datasource_queryset_id is None:
                        query_data = QuerySets.objects.get(queryset_id = query_id,user_id = user_id)
                        query_name=query_data.query_name
                    else:
                        query_data = DataSource_querysets.objects.get(datasource_querysetid = datasource_queryset_id,user_id = user_id,queryset_id = query_id)
                        query_data1 = QuerySets.objects.get(queryset_id = query_id,user_id = user_id)
                        query_name=query_data1.query_name
                except:
                    return Response({'message':'Data not found'},status=status.HTTP_400_BAD_REQUEST)
                query_data2 = QuerySets.objects.get(queryset_id = query_id,user_id = user_id)
                serdt=server_details_check(ServerType1,server_details,file_type,file_data,literal_eval(query_data2.table_names),query_data2.is_custom_sql)                
                if serdt['status']==200:
                    engine=serdt['engine']
                    cur=serdt['cursor']
                else:
                    return Response({'message':serdt['message']},status=serdt['status'])
                st=datetime.datetime.now(utc)
                if dbtype.lower()=="microsoftsqlserver":
                    query="{}".format(query_data.custom_query)
                    if 'limit' in str(query).lower():
                        query=query
                    else:
                        query = query + f' limit {row_limit}'
                    query = query_parsing(query,dbtype,dbtype)
                    result_proxy = cur.execute(query)
                    result_column_values = cur.description
                else:
                    # result_proxy = cur.execute(text(query_data.custom_query))
                    if 'limit' in str(query_data.custom_query).lower():
                        query=query_data.custom_query
                    else:
                        query = query_data.custom_query + f' limit {row_limit}'
                    query = query_parsing(query,dbtype,dbtype)
                    result_proxy = cur.execute(text(query))
                    result_column_values = result_proxy.cursor.description               
                results = result_proxy.fetchall()
                temp_class = Sqlite3_temp_table(query,dbtype)
                table_created = temp_class.create(result_column_values,results,f'join_query{user_id}')
                query_string = f'select * from join_query{user_id} limit {row_limit}'
                # qr_tl=f'select * from join_query{user_id}'
                query_result = temp_class.query(query_string) 

                # Regular expression to extract the part between SELECT and FROM
                pattern = r"SELECT\s+(.*?)\s+FROM"

                # Use re.search to find the match
                match = re.search(pattern, query_data.custom_query,  re.IGNORECASE | re.DOTALL)

                # Extract the matched part
                if match:
                    extracted_part = match.group(1)
                qr_tl=query_data.custom_query.replace(extracted_part,'count(*)')      
                qr_rest = cur.execute(text(qr_tl)) 
                rl_count =qr_rest.fetchall()  
                if query_result['status'] ==200:
                    result = query_result['result_data']
                else:
                    return Response({'message':query_result['message']},status = status.HTTP_400_BAD_REQUEST)
                et=datetime.datetime.now(utc)
                column_names = query_result['columns']
                column_list = [column for column in column_names]
                data = [list(row) for row in result]
                data={
                    "database_id":server_id,
                    "file_id":file_id,
                    "query_set_id" : query_data.queryset_id, 
                    "queryset_name":query_name,
                    "custom_query" :query,
                    "column_data" : column_list,
                    'row_data' : data,
                    "is_custom_query":query_data.is_custom_sql,
                    "query_exection_time":et-st,
                    "total_rows":rl_count[0][0],
                    "no_of_rows":len(data),
                    "no_of_columns":len(column_list),
                    "created_at":query_data.created_at,
                    "updated_at":query_data.updated_at,
                    "query_exection_st":st.time(),
                    "query_exection_et":et.time()
                }
                temp_class.delete(f'join_query{user_id}')
                if file_id is not None and file_id !='':
                    delete_tables_sqlite(cur,engine,serdt['tables'])   
                    cur.close()
                    engine.dispose()
                else:
                    cur.close()
                    #  engine.dispose()      
                return Response(data,status=status.HTTP_200_OK)
        else:
            return Response({"message":tok1['message']},status=status.HTTP_404_NOT_FOUND)



def get_sqlalchemy_type(type_code):
    type_code_map ={
        16: Boolean,
        20: Integer,  # BIGINT in SQLAlchemy is equivalent to Integer in PostgreSQL
        21: Integer,  # SMALLINT in SQLAlchemy is equivalent to Integer in PostgreSQL
        23: Integer,
        700: Float,
        701: Float,
        1700: Numeric,
        1082: Date,
        1083: Time,
        1114: TIMESTAMP,  # TIMESTAMP WITHOUT TIME ZONE in SQLAlchemy is equivalent to DateTime in PostgreSQL
        1184: TIMESTAMP,  # TIMESTAMP WITH TIME ZONE in SQLAlchemy is equivalent to DateTime in PostgreSQL
        1043: String,  # VARCHAR in SQLAlchemy is equivalent to String in PostgreSQL
        127: BIGINT,      # bigint
        52: SMALLINT,
        175: CHAR,        # char
        239: String,      # nchar
        35: TEXT,         # text
        99: TEXT,         # ntext
        173: VARBINARY,   # binary
        165: VARBINARY,
        17: String,
    }
    value =type_code_map.get(type_code, String)()
    return value

# def convert_to_sqlite_syntax(results):
#     converted_results = []
#     for row in results:
#         converted_row = []
#         for item in row:
#             if isinstance(item, str):
#                 converted_row.append(f"'{item}'")
#             elif isinstance(item, (int, float)):
#                 converted_row.append(str(item))
#             elif isinstance(item, datetime.date):
#                 converted_row.append(f"'{item.isoformat()}'")
#             elif isinstance(item, datetime.datetime):
#                 converted_row.append(f"'{item.strftime('%Y-%m-%d %H:%M:%S')}'")
#             else:
#                 converted_row.append(f"'{str(item)}'")
#         converted_results.append(f"({', '.join(converted_row)})")
#     return converted_results
from decimal import Decimal
class Sqlite3_temp_table():
    def __init__(self,main_query,dbtype):
        self.engine = sqlite3.connect('db.sqlite3')
        self.cur = self.engine.cursor()
        self.main_query = main_query
        self.dbtype = dbtype
    def create(self,result_column_values,results,table):
        try:
            if self.dbtype =='microsoftsqlserver':
                column11 =''
                insertvalues = ''
                for i in result_column_values:
                    column11 += f'\"{i[0]}\" {i[1].__name__},'
                    insertvalues += '?,'
            else:
                column11 =''
                insertvalues = ''
                for i in result_column_values:
                    column11 += f'\"{i[0]}\" {get_sqlalchemy_type(i[1])},'
                    insertvalues += '?,'
            create_query = f"CREATE TABLE  {table} ( {column11.rstrip(',')})"
            convert_create_query = query_parsing(create_query,self.dbtype,'sqlite')
            try:
                metadata = MetaData()
                bb = self.cur.execute(convert_create_query)
                self.engine.commit()
                max_res =[]
                for values in results:
                    formatted_values = [float(value) if isinstance(value, Decimal) else value for value in values]
                    max_res.append(formatted_values)
                a1 = self.cur.executemany(f"INSERT INTO {table} VALUES ({insertvalues.rstrip(',')})", max_res)
                self.engine.commit()
            except sqlite3.Error as e:
                self.engine.rollback()
                self.delete(table)
                self.create(result_column_values,results,table)
          
            response = {
                'status': 200,
                "message" : 'table_created'
            }
            # self.cur.close()
        except Exception as e:
            response = {
                "status":400,
                'message':str(e)
            }
        return response
         
    def query(self,query):
        try:
            st = datetime.datetime.now(utc)
            res = self.cur.execute(query)
            et = datetime.datetime.now(utc)
            result_data= res.fetchall()
            # self.cur.close()
            response ={
            "status": 200,
            "columns":[description[0] for description in res.description],
            "result_data" : result_data,
            "st" : st,
            "et" :et
            }
        except Exception as e:
            response ={
            "status": 400,
            "message" : str(e)
            }
        return response
    
    def delete(self,table):
        try:
            a= self.cur.execute(f'DROP TABLE IF EXISTS "{table}";')
            self.engine.commit()
            # self.cur.close()
            # self.engine.close()
            # drop_query =f'drop table {table};'
            # self.cur.execute(drop_query)
            response ={
            "status": 200,
            "message" : 'deleted'
            }
            # self.cur.close()
        except Exception as e:
            response ={
            "status": 400,
            "message" : str(e)
            }
        return response


class Chart_filter(CreateAPIView):
    serializer_class = FilterSerializer
    @transaction.atomic
    def post(self,request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.create_sheet_filters])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                type_of_filter = serializer.validated_data['type_of_filter']
                database_id = serializer.validated_data['database_id']
                file_id = serializer.validated_data['file_id']
                query_set_id =serializer.validated_data['query_set_id']
                datasource_queryset_id = serializer.validated_data['datasource_queryset_id']
                col_name = serializer.validated_data['col_name']
                data_type = serializer.validated_data['data_type']
                format_date = serializer.validated_data['format_date']
                search = serializer.validated_data['search']
            else:
                return Response({'message':'serializer error'},status=status.HTTP_204_NO_CONTENT)
            user_id = tok1['user_id']
            format_date = date_format(format_date)
            con_data =connection_data_retrieve(database_id,file_id,user_id)
            if con_data['status'] ==200:                
                ServerType1 = con_data['serverType1']
                server_details = con_data['server_details']
                file_type = con_data["file_type"]
                file_data =con_data["file_data"]
                dbtype = con_data['dbtype']
            else:
                return Response({'message':con_data['message']},status = status.HTTP_404_NOT_FOUND)
            
            try:
                if type_of_filter.lower() == 'datasource' :
                    query_data = QuerySets.objects.get(queryset_id = query_set_id,user_id = user_id)
                    
                elif(type_of_filter.lower() == 'sheet'and datasource_queryset_id is not None):
                    query_data = DataSource_querysets.objects.get( datasource_querysetid= datasource_queryset_id,user_id = user_id)                    
                else:
                    query_data = QuerySets.objects.get(queryset_id = query_set_id,user_id = user_id)
                query_data1 = QuerySets.objects.get(queryset_id = query_set_id,user_id = user_id)
                serdt=server_details_check(ServerType1,server_details,file_type,file_data,literal_eval(query_data1.table_names),query_data1.is_custom_sql)
                if serdt['status']==200:
                    engine=serdt['engine']
                    cur=serdt['cursor']
                else:
                    return Response({'message':serdt['message']},status=serdt['status'])
            except Exception as e:
                return Response({"messgae" : "Query ID is not Present"},status=status.HTTP_400_BAD_REQUEST)
            if query_data:
                if dbtype.lower()=="microsoftsqlserver":
                    query="{}".format(query_data.custom_query)
                    result_proxy = cur.execute(query)
                    result_column_values = cur.description
                else:
                    result_proxy = cur.execute(text(query_data.custom_query))
                    result_column_values = result_proxy.cursor.description
                results = result_proxy.fetchall()
                temp_class = Sqlite3_temp_table(query_data.custom_query,dbtype)
                if type_of_filter.lower() == 'datasource':
                    table_name_for_temp = f"data_source_table{user_id}"
                    table_created = temp_class.create(result_column_values,results,table_name_for_temp)
                else:
                    table_name_for_temp = f'sheet_table{user_id}'
                    table_created = temp_class.create(result_column_values,results,table_name_for_temp)
                if table_created['status'] ==200:
                    data_sourse_string = f'select * from {table_name_for_temp}'
                else:
                    return Response({'message':table_created['message']},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'Query Set ID is not Present'},status = status.HTTP_400_BAD_REQUEST)
                
                       
            data_type = data_type.split('(')[0]
            if data_type.lower() in integer_list :
                if search:
                    query_string = data_sourse_string.replace('*',f' distinct(\"{col_name}\")') + f' where {col_name} = {search} ' +' order by 1'
                else:
                    query_string = data_sourse_string.replace('*',f' distinct(\"{col_name}\")') + ' order by 1'
                query_result = temp_class.query(query_string)                 
                if query_result['status'] ==200:
                    col_data = query_result['result_data']
                else:
                    return Response({'message':query_result['message']},status = status.HTTP_400_BAD_REQUEST)
            
                row_data =[]   
                for i in col_data:
                    d1 = i[0]
                    row_data.append(d1)
                result_data = row_data
            elif data_type.lower()  in char_list :
                if search:
                    query_string = data_sourse_string.replace('*',f' distinct(\"{col_name}\")') + f' where lower({col_name}) like lower("%{search}%")' +' order by 1'
                    query_string = data_sourse_string.replace('*',f' distinct(\"{col_name}\")') + f' where {col_name} like "%{search}%"' +' order by 1'
                else:
                    query_string = data_sourse_string.replace('*',f' distinct(\"{col_name}\")') + ' order by 1'
                query_result = temp_class.query(query_string)                 
                if query_result['status'] ==200:
                    col_data = query_result['result_data']
                else:
                    return Response({'message':query_result['message']},status = status.HTTP_400_BAD_REQUEST)
            
                row_data =[]   
                for i in col_data:
                    d1 = i[0]
                    row_data.append(d1)
                result_data = row_data
            elif data_type.lower() in bool_list :
                query_string = data_sourse_string.replace('*',f' distinct(\"{col_name}\")') + ' order by 1'
                query_result = temp_class.query(query_string)                 
                if query_result['status'] ==200:
                    col_data = query_result['result_data']
                else:
                    return Response({'message':query_result['message']},status = status.HTTP_400_BAD_REQUEST)
            
                row_data =[]   
                for i in col_data:
                    d1 = i[0]
                    if d1==0:
                        row_data.append(False)
                    else:
                        row_data.append(True)
                result_data = row_data   
                  
            elif 'aggregate' == data_type.lower() or data_type.lower() =='date_aggregate':
                query_string = data_sourse_string.replace('*',f" distinct({format_date}(\"{col_name}\"))" )+ ' order by 1'
                query_result = temp_class.query(query_string)
                if query_result['status'] ==200:
                    col_data = query_result['result_data']
                else:
                    return Response({'message':query_result['message']},status = status.HTTP_400_BAD_REQUEST)
                result_data = list(col_data[0])
            elif data_type.lower() in date_list :
                if search:
                    query_string = data_sourse_string.replace('*',f" distinct(STRFTIME('{format_date}',\"{col_name}\"))") + f" where  STRFTIME('{format_date}',\"{col_name}\") = '{search}'"+' order by 1'
                else:
                    query_string = data_sourse_string.replace('*',f" distinct(STRFTIME('{format_date}',\"{col_name}\"))") + ' order by 1'
                query_result = temp_class.query(query_string)
                if query_result['status'] ==200:
                    col_data = query_result['result_data']
                else:
                    return Response({'message':query_result['message']},status = status.HTTP_400_BAD_REQUEST)
                Months = list(calendar.month_name)[1:]
                result_data =[]   
                for i in col_data:
                    d1 = i[0]
                    result_data.append(d1) 

                result_data = date_data_change(format_date,result_data,1)
                # if format_date == '%m':
                #     result_data = [month_map[month] if month in month_map else None for month in row_data] 
                # else:
                #     result_data = row_data
            else:
                return Response({'message':'data error'},status= status.HTTP_400_BAD_REQUEST)
            Response_data = {
                    "database_id":database_id,
                    "file_id":file_id,
                    "query_set_id":query_set_id,
                    "col_name":col_name,
                    "dtype" : data_type,
                    "col_name":col_name,
                    "col_data" : literal_eval(result_data) if result_data != [""] else []
                }
            delete_query = temp_class.delete(table_name_for_temp)
            if file_id is not None and file_id !='':
                delete_tables_sqlite(cur,engine,serdt['tables'])   
                cur.close()
                engine.dispose()
            else:
                cur.close()
                # engine.dispose()
            if delete_query['status'] ==200:
                    delete_message= delete_query['message']
            else:
                return Response({'message':delete_query['message']},status = status.HTTP_400_BAD_REQUEST)
            return Response(Response_data,status=status.HTTP_200_OK)
        else:
            return Response({"message":tok1['message']},status=status.HTTP_404_NOT_FOUND)
    
    
    serializer_class2 = chartfilter_update_serializer
    @transaction.atomic
    def put(self,request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.edit_sheet_filters])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            serializer = self.serializer_class2(data=request.data)
            if serializer.is_valid(raise_exception=True):
                
                type_of_filter = serializer.validated_data['type_of_filter']
                filter_id = serializer.validated_data['filter_id']
                database_id = serializer.validated_data['database_id']
                file_id = serializer.validated_data['file_id']
                queryset_id = serializer.validated_data['queryset_id']
                datasource_querysetid = serializer.validated_data['datasource_querysetid']
                range_values= serializer.validated_data['range_values']
                select_values = serializer.validated_data['select_values']
                col_name  = serializer.validated_data['col_name']
                data_type = serializer.validated_data['data_type']
                format_date = serializer.validated_data['format_date']

            else:
                return Response({'message':'serializer error'},status=status.HTTP_204_NO_CONTENT)
            user_id = tok1['user_id']
            format_date = date_format(format_date)
            con_data =connection_data_retrieve(database_id,file_id,user_id)
            if con_data['status'] ==200:                
                ServerType1 = con_data['serverType1']
                server_details = con_data['server_details']
                file_type = con_data["file_type"]
                file_data =con_data["file_data"]
                dbtype = con_data['dbtype']
            else:
                    return Response({'message':con_data['message']},status = status.HTTP_404_NOT_FOUND)
            
            try:
                if type_of_filter.lower() == 'datasource' :
                    query_data = QuerySets.objects.get(queryset_id = queryset_id,user_id = user_id)
                    
                elif(type_of_filter.lower() == 'sheet'and datasource_querysetid is not None):
                    query_data = DataSource_querysets.objects.get( datasource_querysetid= datasource_querysetid,user_id = user_id)                    
                else:
                    query_data = QuerySets.objects.get(queryset_id = queryset_id,server_id=database_id,user_id = user_id)
                query_data1 = QuerySets.objects.get(queryset_id = queryset_id,server_id=database_id,user_id = user_id)
                serdt=server_details_check(ServerType1,server_details,file_type,file_data,literal_eval(query_data1.table_names),query_data1.is_custom_sql)            
                if serdt['status']==200:
                    engine=serdt['engine']
                    cur=serdt['cursor']
                else:
                    return Response({'message':serdt['message']},status=serdt['status'])
            except Exception as e:
                return Response({"messgae" : "Query ID is not Present"},status=status.HTTP_400_BAD_REQUEST) 
            if query_data:
                if dbtype.lower()=="microsoftsqlserver":
                    query="{}".format(query_data.custom_query)
                    result_proxy = cur.execute(query)
                    result_column_values = cur.description
                else:
                    result_proxy = cur.execute(text(query_data.custom_query))
                    result_column_values = result_proxy.cursor.description
                results = result_proxy.fetchall()
                temp_class = Sqlite3_temp_table(query_data.custom_query,dbtype)
                if type_of_filter.lower() == 'datasource':
                    table_name_for_temp = f"data_source_table{user_id}"
                    table_created = temp_class.create(result_column_values,results,table_name_for_temp)
                else:
                    table_name_for_temp = f'sheet_table{user_id}'
                    table_created = temp_class.create(result_column_values,results,table_name_for_temp)
                if table_created['status'] ==200:
                    data_sourse_string = f'select * from {table_name_for_temp}'
                else:
                    return Response({'message':table_created['message']},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'Query Set ID is not Present'},status = status.HTTP_400_BAD_REQUEST)
                
                      
            data_type = data_type.split('(')[0]
            if data_type.lower() in integer_list or data_type.lower()  in char_list  :
                query_string = data_sourse_string.replace('*',f' distinct(\"{col_name}\")') + ' order by 1'
                query_result = temp_class.query(query_string)                 
                if query_result['status'] ==200:
                    col_data = query_result['result_data']
                else:
                    return Response({'message':query_result['message']},status = status.HTTP_400_BAD_REQUEST)
            
                row_data =[]   
                for i in col_data:
                    d1 = i[0]
                    row_data.append(d1)
                result_data = row_data
            elif data_type.lower() in bool_list :
                query_string = data_sourse_string.replace('*',f' distinct(\"{col_name}\")') + ' order by 1'
                query_result = temp_class.query(query_string)                 
                if query_result['status'] ==200:
                    col_data = query_result['result_data']
                else:
                    return Response({'message':query_result['message']},status = status.HTTP_400_BAD_REQUEST)
            
                row_data =[]   
                for i in col_data:
                    d1 = i[0]
                    if d1==0:
                        row_data.append(False)
                    else:
                        row_data.append(True)
                result_data = row_data   
                 
            elif 'aggregate' == data_type.lower() or data_type.lower() =='date_aggregate':
                query_string = data_sourse_string.replace('*',f" distinct({format_date}(\"{col_name}\"))" )+ ' order by 1'
                query_result = temp_class.query(query_string)
                if query_result['status'] ==200:
                    col_data = query_result['result_data']
                else:
                    return Response({'message':query_result['message']},status = status.HTTP_400_BAD_REQUEST)
                result_data = list(col_data[0])
            elif data_type.lower() in date_list :
                query_string = data_sourse_string.replace('*',f" distinct(STRFTIME('{format_date}',\"{col_name}\"))") + ' order by 1'
                query_result = temp_class.query(query_string)
                if query_result['status'] ==200:
                    col_data = query_result['result_data']
                else:
                    return Response({'message':query_result['message']},status = status.HTTP_400_BAD_REQUEST)
                result_data =[]   
                for i in col_data:
                    d1 = i[0]
                    result_data.append(d1) 
                result_data = date_data_change(format_date,result_data,1)
                result_data = literal_eval(result_data)
                    # result_data = []
                    # for i in Months:
                    #     if i in row_data:
                    #         result_data.append(i)
            else:
                return Response({'message':'data error'},status= status.HTTP_400_BAD_REQUEST)
            if filter_id is not None:
                if type_of_filter.lower() != 'datasource':
                    aaa = ChartFilters.objects.get(filter_id =filter_id)
                    if range_values:
                        aa = ChartFilters.objects.filter(filter_id =filter_id,user_id =user_id).update(filter_data = range_values,row_data = tuple(result_data),updated_at = datetime.datetime.now())
                    else:
                        aa = ChartFilters.objects.filter(filter_id =filter_id,user_id =user_id  ).update(filter_data = tuple(select_values),row_data = tuple(result_data),updated_at = datetime.datetime.now())
                else:
                    aaa = DataSourceFilter.objects.get(filter_id =filter_id)
                    if range_values:
                        aa = DataSourceFilter.objects.filter(filter_id =filter_id,user_id =user_id ).update(filter_data = range_values,row_data = tuple(result_data),updated_at = datetime.datetime.now())
                    else:
                        aa = DataSourceFilter.objects.filter(filter_id =filter_id,user_id =user_id  ).update(filter_data = tuple(select_values),row_data = tuple(result_data),updated_at = datetime.datetime.now())
                Response_data = {
                    "filter_id" : filter_id              
                }
            else:
                if type_of_filter.lower() == 'datasource':
                    if range_values:
                        aa = DataSourceFilter.objects.create(
                                server_id = database_id,
                                file_id = file_id,
                                user_id=user_id,
                                queryset_id =queryset_id,
                                col_name = col_name,    
                                data_type = data_type,
                                filter_data = range_values,
                                row_data = tuple(result_data),
                                format_type = format_date
                            )
                    else:
                        aa = DataSourceFilter.objects.create(
                            server_id = database_id,
                            file_id = file_id,
                            user_id=user_id,
                            queryset_id =queryset_id,
                            col_name = col_name,    
                            data_type = data_type,
                            filter_data = tuple(select_values),
                            row_data = tuple(result_data),
                            format_type = format_date
                        )
                else:
                    if range_values:

                        aa = ChartFilters.objects.create(
                                server_id = database_id,
                                file_id = file_id,
                                user_id=user_id,
                                datasource_querysetid = datasource_querysetid,
                                queryset_id  = queryset_id,
                                col_name = col_name,    
                                data_type = data_type,
                                filter_data = range_values,
                                row_data = tuple(result_data),
                                format_type = format_date
                            )
                    else:
                        aa = ChartFilters.objects.create(
                                server_id = database_id,
                                file_id = file_id,
                                user_id=user_id,
                                datasource_querysetid = datasource_querysetid,
                                queryset_id  = queryset_id,
                                col_name = col_name,    
                                data_type = data_type,
                                filter_data = tuple(select_values),
                                row_data = tuple(result_data),
                                format_type = format_date
                            )

                Response_data = {
                        "filter_id" : aa.filter_id              
                    }
            delete_query = temp_class.delete(table_name_for_temp)
            if file_id is not None and file_id !='':
                delete_tables_sqlite(cur,engine,serdt['tables'])   
                cur.close()
                engine.dispose()
            else:
                cur.close()
                # engine.dispose()
            if delete_query['status'] ==200:
                    delete_message= delete_query['message']
            else:
                return Response({'message':delete_query['message']},status = status.HTTP_400_BAD_REQUEST)
            return Response(Response_data,status=status.HTTP_200_OK)
        else:
            return Response({"message":tok1['message']},status=status.HTTP_404_NOT_FOUND)


def get_formatted_date_query(db_type,date_column,f1):
    f1 = date_format(f1)
    if f1 =='%m'and db_type=='sqlite':
        query = f""" CASE STRFTIME('{f1}', \"{date_column}\")
                WHEN '01' THEN 'January'
            WHEN '02' THEN 'February'
            WHEN '03' THEN 'March'
            WHEN '04' THEN 'April'
            WHEN '05' THEN 'May'
            WHEN '06' THEN 'June'
            WHEN '07' THEN 'July'
            WHEN '08' THEN 'August'
            WHEN '09' THEN 'September'
            WHEN '10' THEN 'October'
            WHEN '11' THEN 'November'
            WHEN '12' THEN 'December'
            END  """
    elif f1 =='count_distinct':
        if db_type == 'sqlite':
            query = f" count(Distinct STRFTIME('{f1}', \"{date_column}\"))"
        elif db_type == 'mysql':
            query = f" count(Distinct DATE_FORMAT(\"{date_column}\", '%Y-%m-%d')) "
        elif db_type == 'postgres':
            query = f" count(Distinct TO_CHAR({date_column}, 'YYYY-MM-DD'))  "
        elif db_type == 'sqlserver':
            query = f" count(Distinct FORMAT(\"{date_column}\", 'yyyy-MM-dd')) "
        elif db_type == 'oracle':
            query = f" count(Distinct TO_CHAR(\"{date_column}\", 'YYYY-MM-DD')) "
        else:
            raise ValueError("Unsupported database type")
    else:
        if db_type == 'sqlite':
            query = f" STRFTIME('{f1}', \"{date_column}\")"
        elif db_type == 'mysql':
            query = f" DATE_FORMAT(\"{date_column}\", '%Y-%m-%d') "
        elif db_type == 'postgres':
            query = f" TO_CHAR({date_column}, 'YYYY-MM-DD')  "
        elif db_type == 'sqlserver':
            query = f" FORMAT(\"{date_column}\", 'yyyy-MM-dd') "
        elif db_type == 'oracle':
            query = f" TO_CHAR(\"{date_column}\", 'YYYY-MM-DD') "
        else:
            raise ValueError("Unsupported database type")
    return query

    


def Custom_joining_filter(condition,chart_filter_data,type_of_db):
    p = literal_eval(chart_filter_data.filter_data)
    for_range = str(p).replace(',)',')')
    d111 =date_data_change(chart_filter_data.format_type,p,0)
    range_k = literal_eval(for_range) 
    table_name =re.search(r'\((.*?)\)', chart_filter_data.col_name)
    if table_name:
        table_name = table_name.group(1)
        col_name = chart_filter_data.col_name.partition('(')[0]
        col = f'"{col_name}"'
    else:
        table_name=''
        col_name =chart_filter_data.col_name.partition('(')[0]
        col = f'"{col_name}"'
    chart_filter_data.data_type = chart_filter_data.data_type.split('(')[0]
    if  chart_filter_data.data_type.lower() in date_list :
        if isinstance(range_k,list):
            string1 =   f" {condition} STRFTIME('{chart_filter_data.format_type}',\"{chart_filter_data.col_name.partition('(')[0]}\") between '{range_k[0]}' and '{range_k[1]}' " 
            string2 = ''
            string3 = ''
        else:
            string1 =   f" {condition} STRFTIME('{chart_filter_data.format_type}',\"{chart_filter_data.col_name.partition('(')[0]}\") in {d111} " 
            string2 = ''
            string3 = ''

    elif  chart_filter_data.data_type.lower() == 'startswith':
        string1 =f" {condition} lower(\"{col_name}\") like lower('{range_k[0]}%')"
        string2 =  ''
        string3 =  ''
        
    elif chart_filter_data.data_type.lower() == 'endswith':
        string1 = f" {condition} lower(\"{col_name}\") like lower('%{range_k[0]}')"
        string2 = ''
        string3 =  ''
        
    elif  chart_filter_data.data_type.lower() in  integer_list  or chart_filter_data.data_type.lower() in char_list or  chart_filter_data.data_type.lower() in bool_list :
        string1 = f" {condition} \"{col_name}\" in {d111}"
        string2 =  ''
        string3 =  ''
        
    elif chart_filter_data.data_type.lower() == 'aggregate' :
       
        string1 =   ''
        string2 = " "
        string3 = f" having {chart_filter_data.format_type}(\"{col_name}\") between {range_k[0]} and {range_k[1]}"
        
    response_data = {
        "string1":string1,
        "string2":string2,
        "string3":string3
    }
    return response_data


def date_data_change(format,data,value):
    # 0 -decode
    # 1 -encode
    data = literal_eval(data)
    month_map = {
                    '01': 'January',
                    '02': 'February',
                    '03': 'March',
                    '04': 'April',
                    '05': 'May',
                    '06': 'June',
                    '07': 'July',
                    '08': 'August',
                    '09': 'September',
                    '10': 'October',
                    '11': 'November',
                    '12': 'December'
                }
    if value==0:
        if format == '%m':
            month_nums= []
            
            for i in data:
                month_nums.append(list(month_map.keys())[list(month_map.values()).index(i)])
            result_data = tuple(month_nums)
        else:
            result_data = data
    else:
        if format == '%m':
            result_data = [month_map[month] if month in month_map else None for month in data] 
        else:
            result_data = data
    return str(result_data).replace(',)',')')


def Custom_joining_filter1(condition,chart_filter_data,type_of_db):
    p = chart_filter_data.filter_data
    for_range = str(p).replace(',)',')')
    d111=date_data_change(chart_filter_data.format_type,p,0)
    # transformed_data = tuple(f"'{value}'" for value in p)
    # d111 = '(' + ', '.join(transformed_data) + ')'   
    range_k = literal_eval(for_range) 

    chart_filter_data.data_type = chart_filter_data.data_type.split('(')[0]
    if  chart_filter_data.data_type.lower() in date_list :
        if isinstance(range_k,list):
            string1 =   f" {condition} STRFTIME('{chart_filter_data.format_type}',\"{chart_filter_data.col_name.partition('(')[0]}\") between '{range_k[0]}' and '{range_k[1]}'  " 
            string2 = ''
            string3 = ''
        else:
            string1 =   f" {condition} STRFTIME('{chart_filter_data.format_type}',\"{chart_filter_data.col_name.partition('(')[0]}\") in {d111} " 
            string2 = ''
            string3 = ''


    elif  chart_filter_data.data_type.lower() == 'startswith':
        string1 =f" {condition} lower(\"{chart_filter_data.col_name}\") like lower('{range_k[0]}%')"
        string2 =  ''
        string3 =  ''
        
    elif chart_filter_data.data_type.lower() == 'endswith':
        string1 = f" {condition} lower(\"{chart_filter_data.col_name}\") like lower('%{range_k[0]}')"
        string2 = ''
        string3 =  ''
        
    elif  chart_filter_data.data_type.lower() in  integer_list  or chart_filter_data.data_type.lower() in char_list or  chart_filter_data.data_type.lower() in bool_list :
        string1 = f" {condition} \"{chart_filter_data.col_name}\" in {d111}"
        string2 =  ''
        string3 =  ''
        
    elif chart_filter_data.data_type.lower() == 'aggregate' :
       
        string1 =   ''
        string2 = " "
        string3 = f" having {chart_filter_data.format_type}(\"{chart_filter_data.col_name}\") between {range_k[0]} and {range_k[1]}"
        
    response_data = {
        "string1":string1,
        "string2":string2,
        "string3":string3
    }
    return response_data



def data_retrieve_filter(string1,string2,string3,data_sourse_string,col,row,type_of_db):
    try:
        column_string1 = {"col":[],"row":[]}
        response_col1 = {"col":[],"row":[]}
        groupby_string1 = ''
        abc= [col,row]
        check = True if len(abc[0])>0 else False
        for index,col_values in enumerate(abc):
            if index == 0:
                current_value = "col"
            elif index == 1:
                current_value = "row"
            aa= []
            response_col = []
            groupby_string = ''
            for index1,i in enumerate(col_values):
                
                c1 = i[0]
                d1 = i[1]
                f1 = i[2]
                d1  = d1.split('(')[0]               
                if d1.lower() in integer_list   or d1.lower() in char_list :
                    if index1 == 0 and current_value =='col':
                        groupby_string += ' group by '
                        if f1.lower()=='count_distinct':
                            aa.append(f" count(Distinct \"{c1}\")")
                            response_col.append(f" \"CNTD({c1})\"")
                            groupby_string += f" \"CNTD({c1})\","
                        else:
                            aa.append(f" \"{c1}\"")
                            response_col.append(f" \"{c1}\"")
                            groupby_string += f" \"{c1}\","
                    else:
                        if 'group by' in groupby_string:
                            pass
                        else:
                            groupby_string += ' group by '
                        if f1.lower()=='count_distinct':
                            aa.append(f" count(Distinct \"{c1}\")")
                            response_col.append(f" \"CNTD({c1})\"")
                            groupby_string += f" \"CNTD({c1})\"),"
                        else:
                            aa.append(f" \"{c1}\"")
                            response_col.append(f" \"{c1}\"")
                            groupby_string += f" \"{c1}\","
                elif  d1.lower() in bool_list:
                    if index1 == 0 and current_value =='col':
                        groupby_string += ' group by ' 
                        if f1.lower()=='count_distinct':
                            aa.append(f" count(distinct CASE when \"{c1}\" THEN 'True' ELSE 'False' END) AS \"CNTD({c1}:OK)\" ")
                            response_col.append(f" \"CNTD({c1})\"")
                            groupby_string += f" \"CNTD({c1})\","
                        else:
                            aa.append(f" CASE when \"{c1}\" THEN 'True' ELSE 'False' END AS \"{c1}:OK\" ")
                            response_col.append(f" \"{c1}\"")
                            groupby_string += f" \"{c1}\","
                    else:
                        if 'group by' in groupby_string:
                            pass
                        else:
                            groupby_string += ' group by '
                        if f1.lower()=='count_distinct':
                            aa.append(f" count(distinct CASE when \"{c1}\" THEN 'True' ELSE 'False' END) AS \"CNTD({c1}:OK)\" ")
                            response_col.append(f" \"CNTD({c1})\"")
                            groupby_string += f" \"CNTD({c1})\","
                        else:
                            aa.append(f" CASE when \"{c1}\" THEN 'True' ELSE 'False' END AS \"{c1}:OK\" ")
                            response_col.append(f" \"{c1}\"")
                            groupby_string += f" \"{c1}\","
                elif d1.lower() in date_list and len(col_values)!=0:
                    if index1 == 0 and current_value =='col':
                        groupby_string = ' group by '
                        if f1.lower() == 'count_distinct':
                            aa.append(f"{get_formatted_date_query('sqlite',c1,f1)} as \"CNTD({c1}:OK)\"" )
                            response_col.append(f" \"CNTD({c1}:OK)\"" )
                            groupby_string += f"\"CNTD({c1}:OK)\","
                        else:
                            aa.append(f"{get_formatted_date_query('sqlite',c1,f1)} as \"{c1}:OK\"" )
                            response_col.append(f"\"{c1}\"" )
                            groupby_string += f"\"{c1}:OK\"," 
                    else:
                        if 'group by' in groupby_string:
                            pass
                        else:
                            groupby_string = ' group by '
                        if f1.lower() == 'count_distinct':
                            aa.append(f"{get_formatted_date_query('sqlite',c1,f1)} as \"CNTD({c1}:OK)\"" )
                            response_col.append(f" \"CNTD({c1}:OK)\"" )
                            groupby_string += f" \"CNTD({c1}:OK)\","
                        else:
                            aa.append(f"{get_formatted_date_query('sqlite',c1,f1)} as \"{c1}:OK\"" )
                            response_col.append(f"\"{c1}\"" )
                            groupby_string += f"\"{c1}:OK\","     

                elif 'aggregate' == d1.lower():
                    if f1.lower()=='count_distinct':
                        aa.append(f' Count(Distinct \"{c1}\") as \"CNTD({c1})\"')
                        response_col.append(f" \"CNTD({c1})\"" )
                    else:
                        aa.append(f' {f1}(\"{c1}\") as \"{f1}({c1})\"')
                        response_col.append(f"\"{f1}({c1})\"" )
                else:
                    temp11 = {"status":400,'message':'  inputs Errors'}
                    return temp11
            groupby_string1 += groupby_string.replace('group by','') if 'group by' in groupby_string1 else groupby_string

            if index==0:
                column_string1['col'] = aa
            else:
                column_string1['row'] = aa
            if index==0:
                response_col1['col'] = response_col
            else:
                response_col1['row'] = response_col

        combined_values = column_string1['col'] + column_string1["row"]
        a1_combined = ','.join(combined_values)
        if a1_combined:
            query_string = data_sourse_string.replace('*',a1_combined)+ string1 + groupby_string1.strip(',') + string3
        else:
            query_string = data_sourse_string+ string1 + groupby_string1.strip(',') + string3
        query_user = query_parsing(query_string,'sqlite',type_of_db)
        
        temp1 = {
            "status" : 200,
            "column_string" :response_col1,
            "columns" : column_string1['col'],
            "rows" : column_string1['row'],
            "query" : query_string,
            "group_string" : groupby_string1.strip(','),
            "user_col":a1_combined,
            "user_query" : query_user

        }
        return temp1
    except Exception as e:
        temp = {
            "status" : 400,
            "message" : str(e)
        }
    return temp

def literal_eval(data):
    if data==None or data=="":
        data1 = data
    else:
        if isinstance(data,str):
            data1=ast.literal_eval(data)
        else:
            data1=data
    return data1



# def data_retrieve_filter(string1,string2,string3,data_sourse_string,col,row,type_of_db):
#     try:
#         column_string1 = {"col":[],"row":[]}
#         response_col1 = {"col":[],"row":[]}
#         groupby_string1 = ''
#         abc= [col,row]
#         check = True if len(abc[0])>0 else False
#         for index,col_values in enumerate(abc):
#             if index == 0:
#                 current_value = "col"
#             elif index == 1:
#                 current_value = "row"
#             aa= []
#             response_col = []
#             groupby_string = ''
#             for index1,i in enumerate(col_values):
                
#                 c1 = i[0]
#                 d1 = i[1]
#                 f1 = i[2]
#                 d1  = d1.split('(')[0]               
#                 if d1.lower() in integer_list   or d1.lower() in char_list or d1.lower() in bool_list:
#                     if index1 == 0 and current_value =='col':
#                         groupby_string += ' group by '
#                         aa.append(f" \"{c1}\"")
#                         response_col.append(f" \"{c1}\"")
#                         groupby_string += f" \"{c1}\","
#                     else:
#                         if 'group by' in groupby_string:
#                             pass
#                         else:
#                             groupby_string += ' group by '
#                         aa.append(f" \"{c1}\"")
#                         response_col.append(f" \"{c1}\"")
#                         groupby_string += f" \"{c1}\","
#                 elif d1.lower() in date_list and len(col_values)!=0  :
#                     if index1 == 0 and current_value =='col':
#                         groupby_string = ' group by '
#                         aa.append(f"{get_formatted_date_query('sqlite',c1,f1)} as \"{c1}\"" )
#                         response_col.append(f"\"{c1}\"" )
#                         groupby_string += f"\"{c1}\"," 
#                     else:
#                         if 'group by' in groupby_string:
#                             pass
#                         else:
#                             groupby_string = ' group by '
#                         aa.append(f"{get_formatted_date_query('sqlite',c1,f1)} as \"{c1}\"" )
#                         response_col.append(f"\"{c1}\"" )
#                         groupby_string += f"\"{c1}\","     

#                 elif 'aggregate' == d1.lower():
                    
#                     aa.append(f' {f1}(\"{c1}\") as \"{c1}\"')
#                     response_col.append(f"{f1}({c1})" )
#                 else:
#                     temp11 = {"status":400,'message':'  inputs Errors'}
#                     return temp11
#             groupby_string1 += groupby_string.replace('group by','') if 'group by' in groupby_string1 else groupby_string

#             if index==0:
#                 column_string1['col'] = aa
#             else:
#                 column_string1['row'] = aa
#             if index==0:
#                 response_col1['col'] = response_col
#             else:
#                 response_col1['row'] = response_col

#         combined_values = column_string1['col'] + column_string1["row"]
#         a1_combined = ','.join(combined_values)
#         if a1_combined:
#             if type_of_db.lower() =='snowflake':
#                 query_string = data_sourse_string.replace('*',a1_combined).replace('"','')+ string1 + groupby_string1.strip(',').replace('"','') + string3
#             else:
#                 query_string = data_sourse_string.replace('*',a1_combined)+ string1 + groupby_string1.strip(',') + string3
#         else:
#             if type_of_db.lower()=='snowflake':
#                 query_string = data_sourse_string+ string1 + groupby_string1.strip(',').replace('"','') + string3
#             else:
#                 query_string = data_sourse_string+ string1 + groupby_string1.strip(',') + string3
#         query_user = query_parsing(query_string,'sqlite',type_of_db)
        
#         temp1 = {
#             "status" : 200,
#             "column_string" :response_col1,
#             "columns" : column_string1['col'],
#             "rows" : column_string1['row'],
#             "query" : query_string,
#             "group_string" : groupby_string1.strip(','),
#             "user_col":a1_combined,
#             "user_query" : query_user

#         }
#         return temp1
#     except Exception as e:
#         print(e)
#         temp = {
#             "status" : 400,
#             "message" : str(e)
#         }
#     return temp

class Multicolumndata_with_filter(CreateAPIView):  
    serializer_class = GetTableInputSerializer11
    @csrf_exempt
    @transaction.atomic
    def post(self, request,token):
        tok1 = test_token(token)
        if tok1['status']==200:
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid(raise_exception=True):
                col = serializer.validated_data['col']
                row = serializer.validated_data['row']
                query_set_id  = serializer.validated_data['queryset_id']
                datasource_querysetid = serializer.validated_data['datasource_querysetid']
                sheetfilter_querysets_id = serializer.validated_data['sheetfilter_querysets_id']
                filter_id = serializer.validated_data["filter_id"]
                database_id = serializer.validated_data['database_id']
                file_id = serializer.validated_data['file_id']
            else:
                return Response({'message':'serializer error'},status=status.HTTP_204_NO_CONTENT)
            user_id = tok1['user_id']
            con_data =connection_data_retrieve(database_id,file_id,user_id)
            if con_data['status'] ==200:                
                ServerType1 = con_data['serverType1']
                server_details = con_data['server_details']
                file_type = con_data["file_type"]
                file_data =con_data["file_data"]
                dbtype = con_data['dbtype']
            else:
                return Response({'message':con_data['message']},status = status.HTTP_404_NOT_FOUND)
            
            
            try:         
                if datasource_querysetid is not None:
                    query_data = DataSource_querysets.objects.get( datasource_querysetid= datasource_querysetid,user_id = user_id)
                else:
                    query_data = QuerySets.objects.get(queryset_id = query_set_id,user_id = user_id)
                query_data1 = QuerySets.objects.get(queryset_id = query_set_id,user_id = user_id) 
                serdt=server_details_check(ServerType1,server_details,file_type,file_data,literal_eval(query_data1.table_names),query_data1.is_custom_sql)
                if serdt['status']==200:
                    engine=serdt['engine']
                    cur=serdt['cursor']
                else:
                    return Response({'message':serdt['message']},status=serdt['status'])    
            except Exception as e:
                return Response({"messgae" : "Query ID is not Present"},status=status.HTTP_400_BAD_REQUEST)

            if query_data:
                if dbtype.lower()=="microsoftsqlserver":
                    query="{}".format(query_data.custom_query)
                    result_proxy = cur.execute(query)
                    result_column_values = cur.description
                else:
                    result_proxy = cur.execute(text(query_data.custom_query))
                    result_column_values = result_proxy.cursor.description
                results = result_proxy.fetchall()
                temp_sqlite3 = Sqlite3_temp_table(query_data.custom_query,dbtype)
                table_created = temp_sqlite3.create(result_column_values,results,f'multi_table{user_id}')
                if table_created['status'] ==200:
                    data_sourse_string = f'select * from multi_table{user_id}'
                else:
                    return Response({'message':table_created['message']},status=status.HTTP_400_BAD_REQUEST)         
            
            string1 = ''
            string2 = ''
            string3 = ''
            save_string = ''
            for index,filter in enumerate(filter_id):
                try:
                    chart_filter_data = ChartFilters.objects.get(filter_id = filter)
                except:
                    return Response({'message':'chart filter id not present in database'},status=status.HTTP_404_NOT_FOUND)
                
                if chart_filter_data:
                    if index==0:
                        custom_one = Custom_joining_filter1('where',chart_filter_data,dbtype)
                        string1 += custom_one['string1']
                        string2 += custom_one['string2']
                        string3 += custom_one['string3'] 
                    else:
                        custom_one = Custom_joining_filter1('and',chart_filter_data,dbtype)
                        string1 += custom_one['string1']
                        string2 += custom_one['string2']
                        string3 += custom_one['string3']
           
            build_query = data_retrieve_filter(string1,string2,string3,data_sourse_string,col,row,dbtype)
            if build_query["status"] ==200:
                final_query = build_query['query']
            else:
                 return Response({'message':build_query["message"]},status = status.HTTP_400_BAD_REQUEST)
            query_result = temp_sqlite3.query(final_query)            
            if query_result['status'] ==200:
                row_data = query_result['result_data']
            else:
                return Response({'message':query_result['message']},status = status.HTTP_400_BAD_REQUEST)
            
            data = [list(row) for row in row_data]
            db_query_store  = build_query['user_query'].replace(f'multi_table{user_id}',f'({query_data.custom_query}) temp_table')
            # if dbtype.lower()=='snowflake':
            #     db_query_store =db_query_store.replace('"','')
            delete_query = temp_sqlite3.delete(f'multi_table{user_id}')
            if delete_query['status'] ==200:
                    delete_message= delete_query['message']
            else:
                return Response({'message':delete_query['message']},status = status.HTTP_400_BAD_REQUEST)
            
            data = {
                "col_data" : build_query['column_string'],
                "row_data" : data
            }
            if len(build_query['column_string']['col'])>0 or len(build_query['column_string']['row'])>0:
                columns = [col.strip() for col in data["col_data"]["col"]]
                row_labels = [row.strip() for row in data["col_data"]["row"]]

                result = {
                    "col": [],
                    "row": []
                }

                for col in columns:
                    col_index = columns.index(col)
                    
                    result["col"].append({
                        "column": col.replace('"',''),
                        "result_data": [round(float(row[col_index]),2) if type(row[col_index]) is float else row[col_index] for row in data["row_data"] ]
                    })
            
                for row_label in row_labels:
                    row_index = row_labels.index(row_label) + len(columns) 
                    result["row"].append({
                        "col": row_label.replace('"',''),
                        "result_data":  [round(row[row_index],2) if type(row[row_index])is float else row[row_index] for row in data["row_data"] ]
                    })
            else:
                result = {
                    "col": [],
                    "row": []
                }
            if sheetfilter_querysets_id is None:
                abc1 = SheetFilter_querysets.objects.create(
                    datasource_querysetid = datasource_querysetid,
                    queryset_id  = query_set_id,
                    user_id = user_id,
                    server_id = database_id,
                    file_id = file_id,
                    filter_id_list = filter_id,
                    custom_query = db_query_store,
                    columns  = build_query['column_string']['col'],
                    rows = build_query['column_string']['row']
                )
                id = abc1.pk
            else:
                abc1 = SheetFilter_querysets.objects.filter(Sheetqueryset_id =sheetfilter_querysets_id,user_id= user_id).update(
                    queryset_id  = query_set_id,
                    datasource_querysetid = datasource_querysetid,
                    user_id = user_id,
                    server_id = database_id,
                    filter_id_list = filter_id,
                    custom_query = db_query_store,
                    columns  = build_query['column_string']['col'],
                    rows = build_query['column_string']['row'],
                    updated_at = datetime.datetime.now()

                )
                id = sheetfilter_querysets_id
            if file_id is not None and file_id !='':
                delete_tables_sqlite(cur,engine,serdt['tables'])   
                cur.close()
                engine.dispose()
            else:
                cur.close()
                # engine.dispose()
            return Response({'message':'sucess',"sheetfilter_querysets_id" : id,"data" :result},status = status.HTTP_200_OK)
        else:
            return Response({"message":tok1['message']},status=status.HTTP_404_NOT_FOUND)
        
class DataSource_Data_with_Filter(CreateAPIView):  
    serializer_class = GetTableInputSerializer22
    @transaction.atomic
    def post(self, request,token):
        tok1 = test_token(token)
        if tok1['status']==200:
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid(raise_exception=True):
                datasource_queryset_id = serializer.validated_data['datasource_queryset_id']
                query_set_id  = serializer.validated_data['queryset_id']
                filter_id = serializer.validated_data["filter_id"]
                database_id = serializer.validated_data['database_id']
                file_id = serializer.validated_data['file_id']
            else:
                return Response({'message':'serializer error'},status=status.HTTP_204_NO_CONTENT)
            user_id = tok1['user_id']
            con_data =connection_data_retrieve(database_id,file_id,user_id)
            if con_data['status'] ==200:                
                ServerType1 = con_data['serverType1']
                server_details = con_data['server_details']
                file_type = con_data["file_type"]
                file_data =con_data["file_data"]
                dbtype = con_data['dbtype']
            else:
                return Response({'message':con_data['message']},status = status.HTTP_404_NOT_FOUND)
            
            
            try:
                query_data = QuerySets.objects.get(queryset_id = query_set_id,user_id =user_id)
                serdt=server_details_check(ServerType1,server_details,file_type,file_data,literal_eval(query_data.table_names),query_data.is_custom_sql)
                if serdt['status']==200:
                    engine=serdt['engine']
                    cur=serdt['cursor']
                else:
                    return Response({'message':serdt['message']},status=serdt['status'])
            except:
                return Response({"message" : "Query ID is not Present"},status=status.HTTP_400_BAD_REQUEST)
            if query_data:
                if dbtype.lower()=="microsoftsqlserver":
                    query="{}".format(query_data.custom_query)
                    result_proxy = cur.execute(query)
                    result_column_values = cur.description
                else:
                    result_proxy = cur.execute(text(query_data.custom_query))
                    result_column_values = result_proxy.cursor.description
                results = result_proxy.fetchall()
                temp_sqlite3 = Sqlite3_temp_table(query_data.custom_query,dbtype)
                table_created = temp_sqlite3.create(result_column_values,results,f'data_source_table{user_id}')
                if table_created['status'] ==200:
                    data_sourse_string = f'select * from data_source_table{user_id}'
                else:
                    return Response({'message':table_created['message']},status=status.HTTP_400_BAD_REQUEST)
                                    
            
            string1 = ''
            string2 = ''
            string3 = ''
            for index,filter in enumerate(filter_id):
                try:
                    chart_filter_data = DataSourceFilter.objects.get(filter_id = filter)
                except:
                    return Response({'message':'Data Source filter id not present in database'},status=status.HTTP_404_NOT_FOUND)
                
                if chart_filter_data:
                    
                    if index==0:
                        custom_one = Custom_joining_filter('where',chart_filter_data,dbtype)
                        string1 += custom_one['string1']
                        string2 += custom_one['string2']
                        string3 += custom_one['string3'] 
                    else:
                        custom_one = Custom_joining_filter('and',chart_filter_data,dbtype)
                        string1 += custom_one['string1']
                        string2 += custom_one['string2']
                        string3 += custom_one['string3']
            Final_string = data_sourse_string + string1 +string2 + string3
            db_string =query_parsing(Final_string,'sqlite',dbtype)
            user_string = db_string.replace(f'data_source_table{user_id}',f'({query_data.custom_query}) temp1')
            execute_data = temp_sqlite3.query(Final_string)
            if execute_data['status'] ==200:
                rows = execute_data['result_data']
            else:
                return Response({'message':execute_data['message']},status =status.HTTP_404_NOT_FOUND)
            data =[]
            for i in rows:
                a = list(i)
                data.append(a)
            if datasource_queryset_id is  None:
                
                abc = DataSource_querysets.objects.create(
                queryset_id  = query_set_id,
                user_id = user_id,
                server_id = database_id,
                file_id = file_id,
                table_names = query_data.table_names,
                filter_id_list = filter_id,
                is_custom_sql = query_data.is_custom_sql,
                custom_query = user_string
                 )
                id = abc.pk
            else:
                abc = DataSource_querysets.objects.filter( datasource_querysetid = datasource_queryset_id ).update(
                queryset_id  = query_set_id,
                user_id = user_id,
                server_id = database_id,
                file_id = file_id,
                table_names = query_data.table_names,
                filter_id_list = filter_id,
                is_custom_sql = query_data.is_custom_sql,
                custom_query = user_string,
                updated_at = datetime.datetime.now()
                 )
                id = datasource_queryset_id
            final_result = {
                "datasource_queryset_id" : id,
                "query" : user_string
            }

            delete_query = temp_sqlite3.delete(f'data_source_table{user_id}')
            if file_id is not None and file_id !='':
                delete_tables_sqlite(cur,engine,serdt['tables'])   
                cur.close()
                engine.dispose()
            else:
                cur.close()
                # engine.dispose()
            if delete_query['status'] ==200:
                    delete_message= delete_query['message']
            else:
                return Response({'message':delete_query['message']},status = status.HTTP_400_BAD_REQUEST)
            return Response({'message':'sucess',"data" :final_result},status = status.HTTP_200_OK)
            
        else:
            return Response({"message":tok1['message']},status=status.HTTP_404_NOT_FOUND)



class alias_attachment(CreateAPIView):
    serializer_class = alias_serializer
    @transaction.atomic
    def post(self,request,token):
        tok1 = test_token(token)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                tables_list = serializer.validated_data['tables_list']
                count_item = {}
                result_list = []
                for i in tables_list:
                    if i[1] in count_item:
                        count_item[i[1]] +=1
                    else:
                        count_item[i[1]] =0
                    string = f"{i[1]}{str(count_item[i[1]]).replace('0','')}"
                    result_list.append([i[0],i[1],string])
                return Response({'message':'sucess','table_names':result_list},status=status.HTTP_200_OK)
            else:
                return Response({'message':'serializer error'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message':tok1['message']},status=status.HTTP_400_BAD_REQUEST)
        

def alias_to_joins(tables_list,dbtype):
    count_item = {}
    result_list = []
    for i in tables_list:
        table = i.split('.')[0]
        j = i.split('.')[1]
        j=j.strip('"')
        table = table.strip('"')
        if j in count_item:
            count_item[j] =f'{j}({table})'
        else:
            count_item[j] =j
        if dbtype.lower()=='snowflake':
            string = f'\"{table}\".{j} as \"{count_item[j]}\"'
        else:
            string = f'{i} as \"{count_item[j]}\"'
        result_list.append(string)
    return result_list




class get_list_filters(CreateAPIView):
    serializer_class = list_filters
    @transaction.atomic
    def post(self,request,token):
        tok1 = test_token(token)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                type_of_filter = serializer.validated_data['type_of_filter']
                database_id = serializer.validated_data['database_id']
                file_id = serializer.validated_data['file_id']
                query_set_id =serializer.validated_data['query_set_id']
                user_id = tok1['user_id']
                if type_of_filter.lower() == 'datasource':
                    list_filters = DataSourceFilter.objects.filter(queryset_id = query_set_id,user_id = tok1['user_id'])
                else:
                    list_filters = ChartFilters.objects.filter(queryset_id = query_set_id,user_id = tok1['user_id'])
                if list_filters:
                    con_data =connection_data_retrieve(database_id,file_id,user_id)
                    if con_data['status'] ==200:                
                        ServerType1 = con_data['serverType1']
                        server_details = con_data['server_details']
                        file_type = con_data["file_type"]
                        file_data =con_data["file_data"]
                        dbtype = con_data['dbtype']
                    else:
                        return Response({'message':con_data['message']},status = status.HTTP_404_NOT_FOUND)
                    
                    query_data= QuerySets.objects.get(user_id = user_id,queryset_id = query_set_id)
                    serdt=server_details_check(ServerType1,server_details,file_type,file_data,literal_eval(query_data.table_names),query_data.is_custom_sql)
                    try:
                        engine=serdt['engine']
                        cur=serdt['cursor']
                    except:
                        return serdt
                    if dbtype.lower()=="microsoftsqlserver":
                        query="{}".format(query_data.custom_query)
                        execute_stmt = cur.execute(query)
                        col = [column[0] for column in cur.description]
                    else:
                        execute_stmt = cur.execute(text(query_data.custom_query))
                        col = execute_stmt.keys()
                    
                    filters_data = []
                    filters_data = []
                    for filter_item in list_filters:
                        if filter_item.col_name.lower() in col:
                            filters_data.append({
                                    "column_name" : filter_item.col_name,
                                    "filter_id":filter_item.filter_id,
                                })
                        else:
                            if type_of_filter.lower() == 'datasource':
                                DataSourceFilter.objects.filter(filter_id = filter_item.filter_id).delete()
                            else:
                                ChartFilters.objects.filter(filter_id = filter_item.filter_id).delete()
                    if file_id is not None and file_id !='':
                        delete_tables_sqlite(cur,engine,serdt['tables'])   
                        cur.close()
                        engine.dispose()
                    else:
                        cur.close()
                        # engine.dispose()
                    return Response({"filters_data":filters_data},status=status.HTTP_200_OK)
                else:
                    filters_data = []
                    return Response({"filters_data":filters_data},status=status.HTTP_200_OK)
            else:
                return Response({'message':'serializer error'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message':tok1['message']},status=status.HTTP_400_BAD_REQUEST)




class get_table_namesAPI(CreateAPIView):
    serializer_class = get_table_names
    @transaction.atomic
    def post(self,request,token):
        tok1 = test_token(token)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                database_id = serializer.validated_data['database_id']
                query_set_id =serializer.validated_data['query_set_id']
                file_id = serializer.validated_data['file_id']
                search = serializer.validated_data['search']
                user_id = tok1['user_id']
                con_data =connection_data_retrieve(database_id,file_id,user_id)
                if con_data['status'] ==200:                
                    ServerType1 = con_data['serverType1']
                    server_details = con_data['server_details']
                    file_type = con_data["file_type"]
                    file_data =con_data["file_data"]
                    dbtype = con_data['dbtype']
                else:
                    return Response({'message':con_data['message']},status = status.HTTP_404_NOT_FOUND)
                
                query_data = QuerySets.objects.get(queryset_id = query_set_id,user_id = tok1['user_id'])
                serdt=server_details_check(ServerType1,server_details,file_type,file_data,literal_eval(query_data.table_names),query_data.is_custom_sql)
                if serdt['status']==200:
                    engine=serdt['engine']
                    cur=serdt['cursor']
                else:
                    return Response({'message':serdt['message']},status=serdt['status'])  
                list_filters = DataSourceFilter.objects.filter(queryset_id = query_set_id)
                if query_data:
                    if dbtype.lower()=="microsoftsqlserver":
                        query="{}".format(query_data.custom_query)
                        data = cur.execute(query)
                        result = cur.description
                        columns =[]
                        insertvalues = ''
                        for i in result:
                            columns.append({
                                "column":i[0],
                                "data_type" : str(i[1].__name__)
                            })  
                    else:
                        data = cur.execute(text(query_data.custom_query))
                        result = data.cursor.description
                        columns =[]
                        insertvalues = ''
                        for i in result:
                            columns.append({
                                "column":i[0],
                                "data_type" : str(get_sqlalchemy_type(i[1]))
                            })  
                           
                    filter_names = []
                    for i in list_filters:
                        filter_names.append(i.col_name)
                    filtered_data = [item for item in columns if item['column'] not in filter_names and search.lower() in item['column'].lower()]
                if file_id is not None :
                    delete_tables_sqlite(cur,engine,serdt['tables'])   
                    cur.close()
                    engine.dispose()
                else:
                    cur.close()
                    # engine.dispose()
                return Response(filtered_data,status=status.HTTP_200_OK) 
            else:
                return Response({'message':'serializer error'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message':tok1['message']},status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE'])
@transaction.atomic
def filter_delete(request,filter_no,type_of_filter,token):
    role_list=roles.get_previlage_id(previlage=[previlages.delete_sheet_filters,previlages.delete_dashboard_filter])
    tok1 = roles.role_status(token,role_list)
    if tok1['status']==200:
        user_id = tok1['user_id']

        if type_of_filter.lower() != 'datasource':
            aaa = ChartFilters.objects.filter(filter_id =filter_no,user_id=user_id)
            if aaa:
                aaa.delete()
            else:
                return Response({"message":'Data not Found'},status=status.HTTP_404_NOT_FOUND)
        else:
            aaa = DataSourceFilter.objects.filter(filter_id =filter_no,user_id=user_id)
            if aaa:
                aaa.delete()
            else:
                return Response({"message":'Data not Found'},status=status.HTTP_404_NOT_FOUND)
        return_data = {
            "message" : 'Filter Removed Succesfully'
        }
        return Response(return_data,status=status.HTTP_200_OK)
    else:
        return Response({"message":tok1['message']},status=status.HTTP_404_NOT_FOUND)
    



class retrieve_datasource_data(CreateAPIView):
    serializer_class = datasource_retrieve
    @transaction.atomic
    def get(self,request,db_id,queryset_id,token):
        tok1 = test_token(token)
        if tok1['status']==200:
            try:
                data = QuerySets.objects.get(queryset_id = queryset_id,user_id =tok1['user_id'])
            except Exception as e:
                return Response({'message':"Data not Found"},status=status.HTTP_400_BAD_REQUEST)
            datasource_json1 = data.datasource_json
            if datasource_json1 is None:
                json_data = ''
            else:
                request_data = requests.get(datasource_json1)
            result_data={
                "relation_tables":literal_eval(data.joining_conditions),
                "json_data" : request_data.json()
            }
            

            return Response({"dragged_data":result_data},status=status.HTTP_200_OK)      
        else:
            return Response({'message':tok1['message']},status=status.HTTP_400_BAD_REQUEST)

class tables_delete_with_conditions(CreateAPIView):
    serializer_class = tables_delete
    @transaction.atomic
    def post(self,request,token):
        tok1 = test_token(token)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                tables_list = serializer.validated_data['tables_list']
                conditions_list = serializer.validated_data['conditions_list']
                delete_table = serializer.validated_data['delete_table']
            else:
                return Response({'message':'Serializer error'},status=status.HTTP_400_BAD_REQUEST)
            user_id = tok1['user_id']
            filtered_a = [[condition for condition in sublist if delete_table[2] not in condition] for sublist in conditions_list]

            tables_list.remove(delete_table)
            result_data = {
                "tables_list" : tables_list,
                "conditions_list":filtered_a
            }
            return Response({"data":result_data},status=status.HTTP_200_OK)  
        else:
            return Response({'message':tok1['message']},status=status.HTTP_400_BAD_REQUEST)
        





class delete_conition_from_list(CreateAPIView):
    serializer_class = conditions_delete
    @transaction.atomic
    def post(self,request,token):
        tok1 = test_token(token)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                conditions_list = serializer.validated_data['conditions_list']
                delete_condition = serializer.validated_data['delete_condition']
            else:
                return Response({'message':'Serializer error'},status=status.HTTP_400_BAD_REQUEST)
            for index,lists in enumerate(conditions_list):
                for index1,ml in enumerate(lists):
                    if ml==delete_condition:
                        conditions_list[index].pop(index1)
            result_data = {
                "conditions_list":conditions_list
            }
            return Response({"data":result_data},status=status.HTTP_200_OK)  
        else:
            return Response({'message':tok1['message']},status=status.HTTP_400_BAD_REQUEST)
        




class Rename_col_name(CreateAPIView):
    serializer_class = rename_serializer
    @transaction.atomic
    def post(self,request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.rename_dimension_sheet,previlages.rename_measure_sheet])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                database_id = serializer.validated_data['database_id']
                file_id = serializer.validated_data['file_id']
                queryset_id = serializer.validated_data['queryset_id']
                old_col_name = serializer.validated_data['old_col_name']
                new_col_name = serializer.validated_data['new_col_name']
            else:
                return Response({'message':"serializer Error"},status = status.HTTP_400_BAD_REQUEST)
            user_id = tok1['user_id']
            query_data = QuerySets.objects.get(user_id = user_id,queryset_id = queryset_id,server_id = database_id,file_id =file_id)
            datasource_queryset_data = DataSource_querysets.objects.get(user_id = user_id,queryset_id = queryset_id,server_id = database_id,file_id =file_id)
            sheet_data_id = sheet_data.objects.filter(user_id = user_id,queryset_id = queryset_id,server_id = database_id,file_id =file_id)
            dashboard_id = dashboard_data.objects.filter(user_id = user_id,queryset_id = queryset_id,server_id = database_id,file_id =file_id)
            if query_data:                      
                if f'{old_col_name}' in query_data.custom_query:           
                    updated_query = query_data.custom_query.replace(f'as {old_col_name}',f' as {new_col_name}')
                    QuerySets.objects.filter(user_id = user_id,queryset_id = queryset_id,server_id = database_id,file_id =file_id).update(custom_query = updated_query,updated_at = datetime.datetime.now())
                    if f'{old_col_name}' in datasource_queryset_data.custom_query:
                        updated_query11 = datasource_queryset_data.custom_query.replace(f'as {old_col_name}',f' as {new_col_name}')
                        DataSource_querysets.objects.filter(user_id = user_id,queryset_id = queryset_id,server_id = database_id,file_id =file_id).update(custom_query = updated_query11,updated_at = datetime.datetime.now())
                    DataSourceFilter.objects.filter(user_id = user_id,queryset_id = queryset_id,server_id = database_id,col_name = old_col_name,file_id =file_id).update(col_name = new_col_name,updated_at = datetime.datetime.now())
                    ChartFilters.objects.filter(user_id = user_id,queryset_id = queryset_id,server_id = database_id,col_name = old_col_name,file_id =file_id).update(col_name = new_col_name,updated_at = datetime.datetime.now())
                    for i in sheet_data_id:
                        data1 = sheet_data.objects.get(id =i.id)
                        request_data = requests.get(data1.datasrc)
                        json_data = request_data.json()
                        updated_json_data = str(json_data).replace(f'{old_col_name}',f'{new_col_name}')
                        upload_to_s3 = updated_s3file_data(literal_eval(updated_json_data),i.datapath)
                        if upload_to_s3['status'] !=200:
                            return Response({'message':"upload File Error"},status = status.HTTP_400_BAD_REQUEST)
                    for i in dashboard_id:
                        data1 = dashboard_data.objects.get(id =i.id)
                        request_data = requests.get(data1.datasrc)
                        json_data = request_data.json()
                        updated_json_data = str(json_data).replace(f'{old_col_name}',f'{new_col_name}')
                        upload_to_s3 = updated_s3file_data(literal_eval(updated_json_data),i.datapath)
                        if upload_to_s3['status'] !=200:
                            return Response({'message':"upload File Error"},status = status.HTTP_400_BAD_REQUEST)
                    return Response({'message':'Query Updated'},status = status.HTTP_200_OK)
                else:
                    return Response({'message':"column name not found"},status = status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message':"Data not Found"},status =status.HTTP_204_NO_CONTENT)
            
        else:
            return Response({'message':tok1['message']},status=status.HTTP_400_BAD_REQUEST)


def updated_s3file_data(data,file_key):
    json_data = json.dumps(data, indent=4)
    file_buffer = io.BytesIO(json_data.encode('utf-8'))
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY)
    s3.upload_fileobj(file_buffer, Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=str(file_key))
    result = {'status':200}
    return result

class delete_database_stmt(CreateAPIView):
    serializer_class = dashboard_ntfy_stmt
    @transaction.atomic
    def post(self,request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.delete_database])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                database_id = serializer.validated_data['database_id']
                file_id = serializer.validated_data['file_id']
                user_id = tok1['user_id']
                try:
                    if file_id is None or file_id =='':
                        statement_name = 'Database'
                        name = ServerDetails.objects.get(id = database_id,user_id = user_id).display_name
                        query_sets_count = QuerySets.objects.filter(server_id = database_id,user_id =user_id).count()
                        sheets_count = sheet_data.objects.filter(server_id= database_id,user_id=user_id).count()
                        dashboard_count = dashboard_data.objects.filter(server_id= database_id,user_id=user_id).count()
                    else:
                        statement_name = 'File'
                        name = FileDetails.objects.get(id = file_id,user_id=user_id).display_name
                        query_sets_count = QuerySets.objects.filter(file_id = file_id,user_id =user_id).count()
                        sheets_count = sheet_data.objects.filter(file_id = file_id,user_id=user_id).count()
                        dashboard_count = dashboard_data.objects.filter(file_id = file_id,user_id=user_id).count()
                except:
                    return Response({'message':'Data not Found'},status = status.HTTP_400_BAD_REQUEST)
                
                if query_sets_count == 0 and sheets_count ==0 and dashboard_count ==0:
                    statement = f'Are you sure to continue to Delete Database Connection?'
                else:
                    statement = f" The {statement_name} {name} is linked to {sheets_count} charts that appear on {dashboard_count} dashboards and users have {query_sets_count} SQL Queries Using this database open.Are you sure want to continue? Deleting the database will break those objects."

                return Response({'message':statement},status = status.HTTP_200_OK)
            else:
                return Response({'message':"serializer Error"},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':tok1['message']},status=status.HTTP_400_BAD_REQUEST)

class sheet_delete_stmt(CreateAPIView):
    serializer_class = sheet_ntfy_stmt
    @transaction.atomic
    def post(self,request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.delete_sheet])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                sheet_id = serializer.validated_data['sheet_id']
                user_id = tok1['user_id']
                try:
                    sheet_name = sheet_data.objects.get(id = sheet_id ).sheet_name
                except Exception as e:
                    return Response({'message':'Data not Found'},status = status.HTTP_400_BAD_REQUEST)
                
                dashboard_count = dashboard_data.objects.filter(sheet_ids__contains = sheet_id ).count()
                if dashboard_count ==0:
                    statement = f' No Dashboards are Created, Are you sure to continue?'
                else:
                    statement = f'The "{sheet_name}"  is linked to {dashboard_count} dashboard. Are you sure you want to continue?'

                return Response({'message':statement},status = status.HTTP_200_OK)
            else:
                return Response({'message':"serializer Error"},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':tok1['message']},status=status.HTTP_400_BAD_REQUEST)
        

class query_delete_stmt(CreateAPIView):
    serializer_class = query_ntfy_stmt
    @transaction.atomic
    def post(self,request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.delete_custom_sql])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                queryset_id = serializer.validated_data['queryset_id']
                user_id = tok1['user_id']
                try:
                    queryset_name = QuerySets.objects.get(queryset_id = queryset_id,is_custom_sql = True ).query_name
                except Exception as e:
                    return Response({'message':'Data not Found'},status = status.HTTP_400_BAD_REQUEST)
                sheets_count = sheet_data.objects.filter(queryset_id = queryset_id,user_id=user_id).count()
                dashboard_count = dashboard_data.objects.filter(queryset_id =queryset_id,user_id=user_id).count()
                if sheets_count ==0 and dashboard_count ==0:
                    statement = f'No Dependencies on this Query, Are you sure to Continue?'
                else:
                    statement = f' The Query Name  is linked to {sheets_count} charts that appear on {dashboard_count} dashboard. Are you sure you want to continue? Deleting the Query Name will break those objects.'

                return Response({'message':statement},status = status.HTTP_200_OK)
            else:
                return Response({'message':"serializer Error"},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':tok1['message']},status=status.HTTP_400_BAD_REQUEST)


class get_datasource(CreateAPIView):
    serializer_class = GetDataSourceFilter

    def post(self, request, token):
        tok1 = test_token(token)
        if tok1['status'] == 200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                type_filter = serializer.validated_data['type_filter']
                # database_id = serializer.validated_data['database_id']
                filter_no = serializer.validated_data['filter_id']
                search = serializer.validated_data['search']
                user_id = tok1['user_id']
            else:
                return Response({'message': 'serializer error'}, status=status.HTTP_204_NO_CONTENT)

            try:
                if type_filter.lower() != 'datasource':
                    aaa = ChartFilters.objects.get(filter_id=filter_no, user_id=user_id)
                else:
                    aaa = DataSourceFilter.objects.get(filter_id=filter_no, user_id=user_id)
                row_d = literal_eval(aaa.row_data)
                fil_d = literal_eval(aaa.filter_data)
                if search:
                    result = [{'label': item, 'selected': item in fil_d} for item in row_d if search.lower() in item.lower()]
                    result = [{'label': item, 'selected': item in fil_d} for item in row_d if search in item]
                else:
                    result = [{'label': item, 'selected': item in fil_d} for item in row_d]
                array = {'%Y':'year','%m':'month','%d':'day','%H':'hour','%M':'minute','%S':'seconds','%W':'week numbers','%m/%Y':'month/year','%m/%d/%Y':'month/day/year','count_distinct':'count_distinct'}
                return_data = {
                    "data_type":aaa.data_type,
                    'filter_id': filter_no,
                    'format_type':array[aaa.format_type].lower(),
                    "column_name": aaa.col_name,
                    "data_type":aaa.data_type,
                    "result":literal_eval(result)

                }
                return Response(return_data, status=status.HTTP_200_OK)

            except ChartFilters.DoesNotExist:
                return Response({"message": "ChartFilter not found."}, status=status.HTTP_404_NOT_FOUND)
            except DataSourceFilter.DoesNotExist:
                return Response({"message": "DataSourceFilter not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": tok1['message']}, status=status.HTTP_401_UNAUTHORIZED)
        

