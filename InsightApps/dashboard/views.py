from oauth2_provider.models import AccessToken,RefreshToken
import datetime
from pytz import utc
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import *
from django.conf import settings
import requests
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from sqlalchemy import create_engine, inspect, MetaData, Table, text,insert
from sqlalchemy.exc import OperationalError
import json,os
from collections import defaultdict
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
import re
import sqlite3
import base64
import sys
from django.core.paginator import Paginator
from dashboard.columns_extract import server_connection
from dashboard import roles,previlages,columns_extract,Connections,authentication
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Float, Date, Time, DateTime, Numeric,text,TIMESTAMP

def generate_access_from_refresh(refresh_token):
    TOKEN_URL = authentication.TOKEN_URL
    client_id = authentication.CLIENT_ID
    client_secret = authentication.CLIENT_SECRET
    REFRESH_TOKEN = refresh_token

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id': client_id,
        'client_secret': client_secret,
        # Add any additional parameters as needed
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code==200:
        data = {
            'status':200,
            'data':response.json()
        }
    else:
        data = {
            'status':response.status_code,
            'data':response
        }
    return data


def tok_user_check(user):
    if UserProfile.objects.filter(id=user,is_active=True).exists():
        # if license_key.objects.filter(user_id=user,key__isnull=True).exists() or license_key.objects.filter(user_id=user,key=None).exists() or license_key.objects.filter(user_id=user,key='').exists():
        #     data = {
        #         "status":404,
        #         "message":"Liscence key not found for this user, please generate liscence key"
        #     }
        # elif license_key.objects.filter(user_id=user,is_validated=False).exists():
        #     data = {
        #         "status":401,
        #         "message":"Please activate the License key to connect"
        #     }
        # elif license_key.objects.filter(user_id=user,expired_at__gte=datetime.datetime.now(utc)):
        #     data = {
        #         "status":401,
        #         "message":"License key expired, please regenerate new license key"
        #     }
        # else:
        usertable=UserProfile.objects.get(id=user)
        user_role = UserRole.objects.filter(user_id=user).values()
        role_id=[rl['role_id'] for rl in user_role]
        data = {
            "status":200,
            "role_id":role_id,
            "user_id":user,
            "usertable":usertable,
            "username":usertable.username,
            "email":usertable.email
        }
    else:
        data = {
            "status":404,
            "message":"User Not Activated, Please activate the account"
        }
    return data


def token_function(token):
    try:
        token1=AccessToken.objects.get(token=token)
    except:
        data = {"message":"Invalid Access Token",
                "status":404}
        return data
    user = token1.user_id
    rf_token=RefreshToken.objects.get(access_token_id=token1.id,user_id=user)
    # if token1.is_allowed==True:
    #     fn_data=tok_user_check(user)
    #     return fn_data
    if token1.expires < datetime.datetime.now(utc):
        refresh_token=generate_access_from_refresh(rf_token.token)
        if refresh_token['status']==200:
            RefreshToken.objects.filter(id=rf_token.id).delete()
            AccessToken.objects.filter(id=token1.id).delete()
            pass
        else:
            RefreshToken.objects.filter(id=rf_token.id).delete()
            AccessToken.objects.filter(id=token1.id).delete()
            data = {"message":'Session Expired, Please login again',
                    "status":408}
            return data
    else:
        try:
            fn_data=tok_user_check(user)
            return fn_data
        except:
            data = {
                "status":400,
                "message":"Admin not exists/Not assssigned/Role Not created"
            }
            return data      

def test_token(token):
    tok1 = token_function(token)
    return tok1


def encode_string(input_string):
    input_bytes = str(input_string).encode('utf-8')
    encoded_bytes = base64.b64encode(input_bytes)
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def decode_string(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

    # missing_padding = len(encoded_string) % 4
    # if missing_padding != 0:
    #     encoded_string += '=' * (4 - missing_padding)
    # encoded_bytes = str(encoded_string).encode('utf-8')
    # decoded_bytes = base64.b64decode(encoded_bytes)
    # decoded_string = decoded_bytes.decode('utf-8')
    # return decoded_string

def analyze_document_structure(doc):
    schema_info = {}
    for key, value in doc.items():
        schema_info[key] = type(value).__name__
    return schema_info

def database_connection(parameter,engine,dply_name,db_type,hostname,username,encoded_passw,db_name,port,u_id,service_name,server_path,cursor):
    st = ServerType.objects.get(server_type =db_type.upper())
    if dply_name=='' or dply_name==None or dply_name ==' ':
        return Response({'message':"Display Cant be Empty"},status=status.HTTP_406_NOT_ACCEPTABLE)
    elif ServerDetails.objects.filter(user_id=u_id,display_name=dply_name).exists():
        return Response({'message':"Display Name Already Exists"},status=status.HTTP_406_NOT_ACCEPTABLE)
    # else:
    #     return Response({'message':'Server not found'},status=status.HTTP_404_NOT_FOUND)
    
    sd = ServerDetails.objects.create(
        server_type = st.id,
        hostname = hostname,
        username = username,
        password = encoded_passw,
        database = db_name,
        port = port,
        user_id = u_id,
        display_name = dply_name,
        service_name = service_name,
        is_connected=True,
        database_path=server_path
        )
    return Response(
        {
            "message":"Successfully Connected to DB",
            'display_name':sd.display_name,
            "database":
                {
                    "database_id":sd.id,
                    "database_name":sd.database
                }
            }
        ,status=status.HTTP_200_OK)
    
    



def database_connection_update(dply_name,hostname,username,encoded_passw,db_name,port,u_id,service_name,database_id,server_type_id,server_id,server_path):
    if dply_name=='' or dply_name==None or dply_name ==' ':
        return Response({'message':"Display Cant be Empty"},status=status.HTTP_406_NOT_ACCEPTABLE)
    elif ServerDetails.objects.filter(user_id=u_id,display_name=dply_name).exclude(id=database_id).exists():
            return Response({'message':"Display Name Already Exists"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
    sd = ServerDetails.objects.filter(id=server_id).update(
        server_type = server_type_id,
        hostname = hostname,
        username = username,
        password = encoded_passw,
        database = db_name,
        port = port,
        user_id = u_id,
        display_name = dply_name,
        service_name = service_name,
        is_connected=True,
        database_path=server_path,
        updated_at = datetime.datetime.now()
        )
    return Response({'message':"Database Details Updated Successful"},status=status.HTTP_200_OK)
    
class DBConnectionAPI(CreateAPIView):
    
    serializer_class = DataBaseConnectionSerializer
    @csrf_exempt
    @transaction.atomic()
    def post(self, request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.create_database])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            # db_count=ServerDetails.objects.filter(user_id=tok1['user_id']).count()
            # key=license_key.objects.get(user_id=tok1['user_id'])
            # if db_count<key.max_limit:
            #     pass
            # else:
            #     return Response({'message':'Max_limit of connections are done/connections Not allowed'},status=status.HTTP_406_NOT_ACCEPTABLE)
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                db_type = serializer.validated_data['database_type']
                hostname = serializer.validated_data['hostname']
                port = serializer.validated_data['port']
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                db_name = serializer.validated_data['database']
                dply_name = serializer.validated_data['display_name']
                service_name = serializer.validated_data['service_name']
                server_path = serializer.validated_data['path']
                encoded_passw=encode_string(password)
                # file_types = ['excel','csv','pdf','text']
                # if str(db_type).lower() in file_types:
                #     files_data=files_data_extraction(tok1['user_id'],server_path,db_type,dply_name)
                #     return files_data
                if ServerType.objects.filter(server_type =db_type.upper()).exists():
                    ser_data=ServerType.objects.get(server_type=db_type.upper())
                    server_conn=server_connection(username, encoded_passw, db_name, hostname,port,service_name,ser_data.server_type.upper(),server_path)
                    if server_conn['status']==200:
                        engine=server_conn['engine']
                        cursor=server_conn['cursor']
                        parameter=ser_data.server_type.upper()
                        postgres=database_connection(parameter,engine,dply_name,db_type,hostname,username,encoded_passw,db_name,port,tok1['user_id'],service_name,server_path,cursor)
                        return postgres
                    else:
                        return Response(server_conn,status=server_conn['status'])
                else:
                    return Response({'message':"Invalid Server/file Type"},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message':"Serializer Error"},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(tok1,status=tok1['status'])
    
    @transaction.atomic()
    def put(self, request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.edit_database])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                database_id = serializer.validated_data['database_id']
                db_type = serializer.validated_data['database_type']
                hostname = serializer.validated_data['hostname']
                port = serializer.validated_data['port']
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                db_name = serializer.validated_data['database']
                dply_name = serializer.validated_data['display_name']
                service_name = serializer.validated_data['service_name']
                server_path = serializer.validated_data['path']
                try:
                    sd = ServerDetails.objects.get(id=database_id)
                except:
                    return Response({'message':"Invalid Database Id"},status=status.HTTP_404_NOT_FOUND)
                encoded_passw=encode_string(password)
                if ServerType.objects.filter(server_type =db_type.upper()).exists():
                    st = ServerType.objects.get(server_type =db_type.upper())
                    ser_data=ServerType.objects.get(server_type=db_type.upper())
                    server_conn=server_connection(username, encoded_passw, db_name, hostname,port,service_name,ser_data.server_type.upper(),server_path)
                    if server_conn['status']==200:
                        engine=server_conn['engine']
                        cursor=server_conn['cursor']
                        parameter=ser_data.server_type.upper()
                        db_conn_up=database_connection_update(dply_name,hostname,username,encoded_passw,db_name,port,tok1['user_id'],service_name,database_id,st.id,sd.id,server_path)
                        return db_conn_up
                    else:
                        return Response(server_conn,status=server_conn['status'])
                else:
                    return Response({'message':"Invalid Server Type"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({'message':"Serializer Error"},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(tok1,status=tok1['status'])
        

# class GetTablesOfServerDB(CreateAPIView):
@transaction.atomic()
@api_view(['GET'])
def GetTablesOfServerDB(request,token,database_id):
    if request.method=='GET':
        tok1 = test_token(token)
        if tok1['status']==200:
            if ServerDetails.objects.filter(id=database_id).exists():
                sd = ServerDetails.objects.get(id=database_id)
                st = ServerType.objects.get(id=sd.server_type)
                server_conn=server_connection(sd.username,sd.password,sd.database,sd.hostname,sd.port,sd.service_name,st.server_type.upper(),sd.database_path)
                if server_conn['status']==200:
                    engine=server_conn['engine']
                    cursor=server_conn['cursor']
                else:
                    return Response(server_conn,status=server_conn['status'])
                if st.server_type =='POSTGRESQL' or st.server_type =='MYSQL' or st.server_type=="SQLITE":
                    inspector = inspect(engine)
                    schemas = inspector.get_schema_names()
                    ll= []
                    for i in schemas:
                        if i != 'information_schema':
                            table_names = inspector.get_table_names(schema=i)
                            
                            for table_name in table_names:
                                columns = inspector.get_columns(table_name,schema=i)
                                col = []
                                for column in columns:
                                    col.append({"columns": column['name'].lower(), "datatypes": str(column['type']).lower()})
                                ll.append({"schema":i,"table":table_name,"columns":col})
                        pass
                    return Response(
                        {
                            "message":"Successfully Connected to DB",
                            "data":ll,
                            'display_name':sd.display_name,
                            "database":
                                {
                                    "database_id":sd.id,
                                    "database_name":sd.database
                                }
                            }
                        ,status=status.HTTP_200_OK)
                elif st.server_type =='ORACLE':
                    inspector = inspect(engine)
                    table_names = inspector.get_table_names(schema=sd.username)
                    ll=[]    
                    for table_name in table_names:
                        columns = inspector.get_columns(table_name)
                        col = []
                        for column in columns:
                            col.append({"columns": column['name'].lower(), "datatypes": str(column['type']).lower()})
                        ll.append({"schema":sd.username,"table":table_name,"columns":col})
                        
                    return Response(
                        {
                            "message":"Successfully Connected to DB",
                            "data":ll,
                            'display_name':sd.display_name,
                            "database":
                                {
                                    "database_id":sd.id,
                                    "database_name":sd.database
                                }
                            }
                        ,status=status.HTTP_200_OK)
                elif st.server_type=="MONGODB":
                    db=engine
                    final_list={}
                    colms=[]
                    final_ls=[]
                    collections = db.list_collection_names()
                    for collection_name in collections:
                        final_list['schema']=None
                        final_list['table']=collection_name
                        collection = db[collection_name]
                        documents = collection.find()
                        for field in documents:
                            cllist=[]
                            colms.append({'columns':cllist.append(field),'datatypes':None})
                        final_list['columns']=colms
                    final_ls.append(final_list)
                    return Response(
                        {
                            "message":"Successfully Connected to DB",
                            "data":final_ls,
                            'display_name':sd.display_name,
                            "database":
                                {
                                    "database_id":sd.id,
                                    "database_name":sd.database
                                }
                            }
                        ,status=status.HTTP_200_OK)
                elif st.server_type.upper()=="MICROSOFTSQLSERVER":
                    tables_query = """
                    SELECT 
                        TABLE_SCHEMA,
                        TABLE_NAME
                    FROM 
                        INFORMATION_SCHEMA.TABLES
                    WHERE 
                        TABLE_TYPE = 'BASE TABLE'
                    """
                    cursor.execute(tables_query)
                    tables = cursor.fetchall()
                    schema_info = {}
                    for table in tables:
                        schema = table.TABLE_SCHEMA
                        table_name = table.TABLE_NAME
                        if schema not in schema_info:
                            schema_info[schema] = {}
                        columns_query = f"""
                        SELECT 
                            COLUMN_NAME,
                            DATA_TYPE
                        FROM 
                            INFORMATION_SCHEMA.COLUMNS
                        WHERE 
                            TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table_name}'
                        ORDER BY 
                            ORDINAL_POSITION
                        """
                        cursor.execute(columns_query)
                        columns = cursor.fetchall()
                        schema_info[schema][table_name] = [(column.COLUMN_NAME, column.DATA_TYPE) for column in columns]
                    formatted_data = []
                    for schema_name, tables in schema_info.items():
                        for table_name, columns in tables.items():
                            table_entry = {"schema": schema_name, "table": table_name, "columns": []}
                            for column_name, data_type in columns:
                                column_entry = {"columns": column_name, "datatypes": data_type}
                                table_entry["columns"].append(column_entry)
                            formatted_data.append(table_entry)
                    return Response(
                        {
                            "message":"Successfully Connected to DB",
                            "data":formatted_data,
                            'display_name':sd.display_name,
                            "database":
                                {
                                    "database_id":sd.id,
                                    "database_name":sd.database
                                }
                            }
                        ,status=status.HTTP_200_OK)
                else:
                    return Response({'message':'SERVER not found'},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message':"Invalid Data Base ID"},status=status.HTTP_404_NOT_FOUND)                           
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({'message':'Method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
def set_list_elements(new_list):
    global list_elements
    if len(new_list) == 1 and len(new_list[0]) == 2:
        list_elements = new_list
    else:
        raise ValueError("Invalid list format. It should be [['schema_name', 'table_name']]")

        
class GetTableRelationShipAPI(CreateAPIView):
    serializer_class = GetColumnFromTableSerializer
    
    @transaction.atomic()
    def post(self, request,token):
        tok1 = test_token(token)
        if tok1['status']==200:
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid(raise_exception=True):
                db_id = serializer.validated_data['database_id']
                tables = serializer.validated_data['tables']
                conditions = serializer.validated_data['condition']
                # datatype = serializer.validated_data['datatype']

                
                sd = ServerDetails.objects.get(id=db_id)
                st = ServerType.objects.get(id=sd.server_type)
                server_conn=server_connection(sd.username,sd.password,sd.database,sd.hostname,sd.port,sd.service_name,st.server_type.upper(),sd.database_path)
                if server_conn['status']==200:
                    engine=server_conn['engine']
                    cursor=server_conn['cursor']
                else:
                    return Response(server_conn,status=server_conn['status'])
                # Check the connection status
                if conditions == []:
                    try:
                        inspector = inspect(engine)

                        l=[]
                        for schema,table_name in tables:
                            columns = inspector.get_columns(table_name = table_name,schema = schema)
                            col = []
                            for column in columns:
                                col.append({"columns": column['name'].lower(), "datatypes": str(column['type']).lower()})
                            l.append({"table":f'{schema}.{table_name}',"columns":col})
                        
                        if conditions == "" or conditions == []:
                            try:
                                # Iterate through the columns of the Table1 
                                for column1 in l[0]["columns"]:
                                    # Iterate through the columns of the Table2
                                    for column2 in l[1]["columns"]:
                                        # Check if the column names and data types match
                                        if column1["columns"] == column2["columns"] and column1["datatypes"] == column2["datatypes"]:
                                            l.append({'relation':
                                                {
                                                    "datatype":column2['datatypes'],
                                                    "tables":[l[0]['table'],l[1]['table']],
                                                    "condition":["{}.{} = {}.{}".format(l[0]['table'],column1["columns"],l[1]['table'],column2["columns"])]
                                                }
                                            })
                                            return Response(l)
                            except:
                                pass
                            l.append({'relation':
                                {
                                    "datatype":"",
                                    "tables":[l[0]['table'],l[1]['table']],
                                    "condition":[]
                                }
                            })
                            return Response(l)
                        else:
                            l.append({'relation':
                                {
                                    "datatype":"",
                                    "tables":[l[0]['table'],l[1]['table']],
                                    "condition":[condition]
                                }
                            })
                            return Response(l)
                    except Exception as e:
                        return Response({'message':f"Connection error: {e}"})
                else:
                    inspector = inspect(engine)
                    l=[]
                    for schema,table_name in tables:
                        columns = inspector.get_columns(table_name = table_name,schema = schema)
                        col = []
                        for column in columns:
                            col.append({"columns": column['name'].lower(), "datatypes": str(column['type']).lower()})
                        l.append({"table":f'{schema}.{table_name}',"columns":col})
                    
                    # Check if the data types of the condition field match in both tables
                    table1_schema, table1_name = tables[0]
                    table2_schema, table2_name = tables[1]

                    # Extract column names and check their existence
                    for condition in conditions:
                        # Extract column names from the condition
                        table1_column = condition[0].split('=')[0].strip().split('.')[-1]
                        table2_column = condition[0].split('=')[1].strip().split('.')[-1]
                        
                        # Get the list of columns for the specified table
                        column1 = inspector.get_columns(table1_name, schema=table1_schema)

                        # Find the index of the column you're interested in
                        column1_index = next((i for i, col in enumerate(column1) if col['name'] == table1_column), None)
                        
                        column2 = inspector.get_columns(table2_name, schema=table2_schema)

                        # Find the index of the column you're interested in
                        column2_index = next((i for i, col in enumerate(column2) if col['name'] == table2_column), None)

                        if column1_index is not None and column2_index is not None:
                            col1_datatype = column1[column1_index]['type']
                            col2_datatype = column2[column2_index]['type']
                            if str(col1_datatype).split('(')[0].lower() == str(col2_datatype).split('(')[0].lower():
                                pass
                            else:
                                return Response({'message':"Field Datatypes Mismatch {} & {}".format(str(col1_datatype).split('(')[0].lower(),str(col2_datatype).split('(')[0].lower())},status=status.HTTP_400_BAD_REQUEST)
                        else:
                            # Handle the case where one or both columns are not found
                            if column1_index is None:
                                return Response({'message':f"Column '{table1_column}' not found in table '{table1_name}'."},status=status.HTTP_404_NOT_FOUND)
                            if column2_index is None:
                                return Response({'message':f"Column '{table2_column}' not found in table '{table2_name}'."},status=status.HTTP_404_NOT_FOUND)
                        
                    l.append({'relation':
                            {
                                "datatype":str(col1_datatype).split('(')[0],
                                "tables":tables,
                                "condition": conditions
                            }
                        })
                    return Response(l)
            return Response({'message':"Serializer Error"},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(tok1,status=tok1['status'])
        
            
    @transaction.atomic()
    def put(self, request,token):
        tok1 = test_token(token)
        if tok1['status']==200:
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid(raise_exception=True):
                db_id = serializer.validated_data['database_id']
                tables = serializer.validated_data['tables']

                try:
                    set_list_elements(tables)
                except ValueError as e:
                    return Response({"message":f'{e}'},status=status.HTTP_406_NOT_ACCEPTABLE)
                
                try:
                    sd = ServerDetails.objects.get(id=int(db_id))
                except:
                    return Response({'message':"Invalid Database ID"},status=status.HTTP_404_NOT_FOUND)
                
                try:
                    st = ServerType.objects.get(id=sd.server_type)
                except:
                    return Response({'message':"Server Type Not Found"},status=status.HTTP_404_NOT_FOUND)
                
                for schema,table in tables:
                    table_name = f'{schema}.{table}'

                server_conn=server_connection(sd.username,sd.password,sd.database,sd.hostname,sd.port,sd.service_name,st.server_type.upper(),sd.database_path)
                if server_conn['status']==200:
                    engine=server_conn['engine']
                    connection=server_conn['cursor']
                else:
                    return Response(server_conn,status=server_conn['status'])
                if st.server_type.upper()=="POSTGRESQL" or st.server_type =='MYSQL' or st.server_type=="SQLITE":
                    query = text('SELECT * FROM "{}"."{}"'.format(schema,table))
                    inspector = inspect(engine)
                    columns = inspector.get_columns(table,schema=schema)
                elif st.server_type.upper()=="ORACLE":
                    query = text("SELECT * FROM {}".format(table_name))
                    inspector = inspect(engine)
                    columns = inspector.get_columns(table_name)

                result = connection.execute(query)
                col = []
                for column in columns:
                    col.append({"table":table_name,"columns": column['name'].lower(), "datatypes": str(column['type']).lower()})
                rows = result.fetchall()
                data =[]
                for i in rows:
                    a = list(i)
                    data.append(a)
                return Response({"column_data":col,"row_data":data})

            return Response({'message':"Serializer Error"},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(tok1,status=tok1['status'])

class ListofActiveServerConnections(CreateAPIView):
    
    serializer_class = SearchFilterSerializer
    @transaction.atomic()
    def put(self, request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.view_database])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid(raise_exception=True):
                # Search Filter Only works on Display Name Column in Server Details
                search = serializer.validated_data['search']
                page_no = serializer.validated_data['page_no']
                page_count = serializer.validated_data['page_count']
                
                if ServerDetails.objects.filter(user_id=tok1['user_id'],is_connected=True).exists() or FileDetails.objects.filter(user_id=tok1['user_id']).exists():
                
                    if search =='':
                        details = ServerDetails.objects.filter(user_id=tok1['user_id'],is_connected=True).values().order_by('-updated_at')
                        filedetai = FileDetails.objects.filter(user_id=tok1['user_id'],quickbooks_user_id=None).values().order_by('-updated_at')
                    else:
                        details = ServerDetails.objects.filter(user_id=tok1['user_id'],is_connected=True,display_name__icontains=search).values().order_by('-updated_at')
                        filedetai = FileDetails.objects.filter(user_id=tok1['user_id'],display_name__icontains=search,quickbooks_user_id=None).values().order_by('-updated_at')
                    l =[]
                    for i in details:
                        st = ServerType.objects.get(id=i['server_type'])
                        data = {
                            "file_id":None,
                            "file_type":None,
                            "database_id":i['id'],
                            "server_type":st.server_type,
                            "database_type":st.server_type.lower(),
                            "hostname":i['hostname'],
                            "database":i['database'],
                            "port" :i['port'],
                            "username":i['username'],
                            "service_name":i['service_name'],
                            "display_name":i['display_name'],
                            "is_connected":i['is_connected'],
                            "created_by":tok1['username'],
                            "created_at" : i['created_at'].date(),
                            "updated_at" : i['updated_at'].date()
                        }
                        l.append(data)
                    for h in filedetai:
                        st = FileType.objects.get(id=h['file_type'])
                        data1 = {
                            "file_id":h['id'],
                            "file_type":st.file_type,
                            "database_id":None,
                            "server_type":st.file_type,
                            "database_type":st.file_type.lower(),
                            "hostname":None,
                            "database":None,
                            "port" :None,
                            "username":None,
                            "service_name":None,
                            "display_name":h['display_name'],
                            "is_connected":None,
                            "created_by":tok1['username'],
                            "created_at" : h['uploaded_at'].date(),
                            "updated_at" : h['updated_at'].date()
                        }
                        l.append(data1)
                    try:
                        paginator = Paginator(l,page_count)
                        page = request.GET.get("page",page_no)
                        object_list = paginator.page(page)
                        re_data = list(object_list)
                        data1 = {
                            "status":200,
                            "sheets":re_data,
                            "total_pages":paginator.num_pages,
                            "items_per_page":page_count,
                            "total_items":paginator.count
                        }
                        return Response(data1,status=status.HTTP_200_OK)
                    except:
                        return Response({'message':'Empty page, data not exists'},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'connection':[]},status=status.HTTP_200_OK)
            else:
                return Response({'message':"Serialzer Error"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(tok1,status=tok1['status'])


def custom_query_data(row_limit,paramet,server_id,custom_query,u_id,datasorce_queryset_id,server_type,query_name,parameter,queryset_id):
    if paramet=="server":
        server_id1=server_id
        file_id=None
        try:
            sd = ServerDetails.objects.get(id=server_id1)
        except:
            return Response({'message':"Invalid Database ID"},status=status.HTTP_404_NOT_FOUND)
        try:
            st = ServerType.objects.get(id=sd.server_type)
        except Exception as e:
            return Response({'message':"Server Type Not Found"},status=status.HTTP_404_NOT_FOUND)
        
        server_conn=server_connection(sd.username,sd.password,sd.database,sd.hostname,sd.port,sd.service_name,st.server_type.upper(),sd.database_path)
        if server_conn['status']==200:
            engine=server_conn['engine']
            connection=server_conn['cursor']
        else:
            return Response(server_conn,status=server_conn['status'])
    else:
        server_id1=None
        file_id=server_id
        file_type=server_type
        try:
            filedata = FileDetails.objects.get(user_id=u_id,id=file_id)
        except:
            return Response({'message':"Invalid file ID"},status=status.HTTP_404_NOT_FOUND)
        files_data=columns_extract.file_details(file_type,filedata)
        if files_data['status']==200:
            engine=files_data['engine']
            connection=files_data['cursor']
            tables=files_data['tables_names']
        else:
            return Response({'message':files_data['message']},status=files_data['status'])

    start_time=datetime.datetime.now(utc)
    # Execute a query
    try: 
        if server_type=="MICROSOFTSQLSERVER":
            clean_query_string = re.sub('[;\[\]]', '', custom_query)
            query1 = text(clean_query_string)
            if 'limit' in str(query1).lower():
                query=query1
            else:
                query = "{} limit {}".format(query1,row_limit)
            result = connection.execute(query)
            columns_info = connection.description
            column_list = [column[0] for column in columns_info]
            data_type_list = [data_type[1].__name__ for data_type in columns_info]
            rows = result.fetchall()

            query12 = "{}".format(query1)
            result12 = connection.execute(query12)
            columns_info12 = connection.description
            column_list12 = [column[0] for column in columns_info12]
            data_type_list12 = [data_type[1].__name__ for data_type in columns_info12]
            rows12 = result12.fetchall()
        else:
            clean_query_string = re.sub(';', '', custom_query)
            if 'limit' in str(clean_query_string).lower():
                query11=clean_query_string
            else:
                query11 = "{} limit {}".format(clean_query_string,row_limit)
            query = text(query11)
            result = connection.execute(query)
            column_names = result.keys()
            column_list = [column for column in column_names]
            rows = result.fetchall()

            query12 = text(clean_query_string)
            result12 = connection.execute(query12)
            column_names12 = result12.keys()
            column_list12 = [column for column in column_names12]
            rows12 = result12.fetchall()
    except Exception as e:
        return Response({'message':f'{e}'},status=status.HTTP_400_BAD_REQUEST)
    
    column_counts = {}  #### ambigious error for repeated column names in query.
    colum_ambi_list=[]
    for column in column_list:
        if column in column_counts:
            column_counts[column] += 1
        else:
            column_counts[column] = 1
    repeated_columns = {column: count for column, count in column_counts.items() if count > 1}
    for column, count in repeated_columns.items():
        colum_ambi_list.append(column)
        # print(f"{column}: {count} times")
    if colum_ambi_list==[]:
        pass
    else:
        return Response({'message':'column reference {} is ambiguous'.format(colum_ambi_list[0])},status=status.HTTP_406_NOT_ACCEPTABLE)
 
    data =[]
    for i in rows:
        a = list(i)
        data.append(a)
    
    row_count=[]
    for m in rows12:
        a12 = list(m)
        row_count.append(a12)
        
    if parameter=="SAVE":
        if queryset_id=='' or queryset_id==None:
            qs=QuerySets.objects.create(
                user_id = u_id,
                server_id = server_id1,
                file_id=file_id,
                is_custom_sql = True,
                custom_query = clean_query_string,
                query_name=query_name
            )
            qs.save()
        else:
            QuerySets.objects.filter(queryset_id=queryset_id).update(
                    custom_query = clean_query_string,query_name=query_name,updated_at=datetime.datetime.now(),
                    file_id=file_id,user_id=u_id)
            qs = QuerySets.objects.get(queryset_id=queryset_id)
    elif parameter=="UPDATE":
        if queryset_id=='' or queryset_id==None:
            return Response({'message':'Empty queryset_id field is not accepted'},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            if file_id==None:
                QuerySets.objects.filter(queryset_id=queryset_id,server_id=server_id1,user_id=u_id).update(
                    custom_query = clean_query_string,query_name=query_name,updated_at=datetime.datetime.now())
            else:
                QuerySets.objects.filter(queryset_id=queryset_id,file_id=file_id,user_id=u_id).update(
                    custom_query = clean_query_string,query_name=query_name,updated_at=datetime.datetime.now())
            qs = QuerySets.objects.get(queryset_id=queryset_id)
    elif parameter=="GET":
        qs = QuerySets.objects.get(queryset_id=queryset_id)

    end_time=datetime.datetime.now(utc)
    data={
        "database_id":server_id1,
        "file_id":file_id,
        "query_name":query_name,
        "datasorce_queryset_id":datasorce_queryset_id,
        "query_set_id" : qs.queryset_id, 
        "custom_query" : qs.custom_query,
        "column_data" : column_list,
        'row_data' : data,
        "is_custom_query":qs.is_custom_sql,
        "query_exection_time":end_time-start_time,
        "total_rows":len(row_count),
        "no_of_rows":len(data),
        "no_of_columns":len(column_list),
        "created_at":qs.created_at,
        "updated_at":qs.updated_at,
        "query_exection_st":start_time.time(),
        "query_exection_et":end_time.time()
        }
    if paramet!="server":
        columns_extract.delete_tables_sqlite(connection,engine,files_data['tables_names'])
    else:
        pass
    return Response(data,status=status.HTTP_200_OK)

class CustomSQLQuery(CreateAPIView):
    serializer_class = CustomSQLSerializer
    
    @transaction.atomic()
    def post(self,request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.create_custom_sql,previlages.view_custom_sql])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                custom_query = serializer.validated_data['custom_query']
                server_id = serializer.validated_data['database_id']
                query_name = serializer.validated_data['query_name']
                queryset_id = serializer.validated_data['queryset_id']
                file_id = serializer.validated_data['file_id']
                row_limit = serializer.validated_data['row_limit']
                para="SAVE"
                # quer=''
                dq_id=None
                file_p="file"
                server_p="server"
                if file_id==None or file_id=='':
                    if ServerDetails.objects.filter(id=server_id).exists():
                        srtb=ServerDetails.objects.get(id=server_id)
                        srtyp=ServerType.objects.get(id=srtb.server_type)
                    else:
                        return Response({'message':'Server id not exists'},status=status.HTTP_404_NOT_FOUND)
                    final_data=custom_query_data(row_limit,server_p,server_id,custom_query,tok1['user_id'],dq_id,srtyp.server_type.upper(),query_name,para,queryset_id)
                    return final_data
                else:
                    if FileDetails.objects.filter(id=file_id).exists():
                        file_db_data=FileDetails.objects.get(id=file_id)
                        file_data=FileType.objects.get(id=file_db_data.file_type)
                    else:
                        return Response({'message':'file_details_id/file_type not exists'},status=status.HTTP_404_NOT_FOUND)
                    final_data=custom_query_data(row_limit,file_p,file_db_data.id,custom_query,tok1['user_id'],dq_id,file_data.file_type.upper(),query_name,para,queryset_id)
                    return final_data
            else:
                return Response({"message":"Serializer Error"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(tok1,status=tok1['status'])
        

    @transaction.atomic()
    def put(self,request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.edit_custom_sql,previlages.view_custom_sql])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                custom_query = serializer.validated_data['custom_query']
                server_id = serializer.validated_data['database_id']
                query_name = serializer.validated_data['query_name']
                queryset_id = serializer.validated_data['queryset_id']
                file_id = serializer.validated_data['file_id']
                row_limit = serializer.validated_data['row_limit']
                para="UPDATE"
                file_p="file"
                server_p="server"
                if file_id==None or file_id=='':
                    if ServerDetails.objects.filter(id=server_id).exists():
                        srtb=ServerDetails.objects.get(id=server_id)
                        srtyp=ServerType.objects.get(id=srtb.server_type)
                    else:
                        return Response({'message':'Server id not exists'},status=status.HTTP_404_NOT_FOUND)
                    if DataSource_querysets.objects.filter(queryset_id=queryset_id).exists():
                        quer_tb=DataSource_querysets.objects.get(queryset_id=queryset_id,server_id=server_id,user_id=tok1['user_id'])
                        datasorce_queryset_id=quer_tb.datasource_querysetid
                    else:
                        datasorce_queryset_id=None
                    final_data=custom_query_data(row_limit,server_p,server_id,custom_query,tok1['user_id'],datasorce_queryset_id,srtyp.server_type.upper(),query_name,para,queryset_id=queryset_id)
                    return final_data
                else:
                    if FileDetails.objects.filter(id=file_id).exists():
                        file_db_data=FileDetails.objects.get(id=file_id)
                        file_data=FileType.objects.get(id=file_db_data.file_type)
                    else:
                        return Response({'message':'file_details_id/file_type not exists'},status=status.HTTP_404_NOT_FOUND)
                    if DataSource_querysets.objects.filter(queryset_id=queryset_id).exists():
                        quer_tb=DataSource_querysets.objects.get(queryset_id=queryset_id,file_id=file_id,user_id=tok1['user_id'])
                        datasorce_queryset_id=quer_tb.datasource_querysetid
                    else:
                        datasorce_queryset_id=None
                    final_data=custom_query_data(row_limit,file_p,file_db_data.id,custom_query,tok1['user_id'],datasorce_queryset_id,file_data.file_type.upper(),query_name,para,queryset_id=queryset_id)
                    return final_data
            else:
                return Response({"message":"Serializer Error"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(tok1,status=tok1['status'])
        

class custom_query_get(CreateAPIView):
    serializer_class=CustomSQLSerializer

    @transaction.atomic()
    def post(self,request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.view_custom_sql])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                server_id = serializer.validated_data['database_id']
                queryset_id = serializer.validated_data['queryset_id']
                file_id = serializer.validated_data['file_id']
                row_limit = serializer.validated_data['row_limit']
                para="GET"
                file_p="file"
                server_p="server"
                if queryset_id=='' or queryset_id==None:
                    return Response({'message':'Empty queryset_id field is not accepted'},status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    try:
                        qrset=QuerySets.objects.get(user_id=tok1['user_id'],queryset_id=queryset_id)
                    except:
                        return Response({'message','Data not exists'},status=status.HTTP_404_NOT_FOUND)
                if file_id==None or file_id=='':
                    if ServerDetails.objects.filter(id=server_id).exists():
                        srtb=ServerDetails.objects.get(id=server_id)
                        srtyp=ServerType.objects.get(id=srtb.server_type)
                    else:
                        return Response({'message':'Server id not exists'},status=status.HTTP_404_NOT_FOUND)
                    if DataSource_querysets.objects.filter(queryset_id=queryset_id).exists():
                        quer_tb=DataSource_querysets.objects.get(queryset_id=queryset_id,server_id=server_id,user_id=tok1['user_id'])
                        datasorce_queryset_id=quer_tb.datasource_querysetid
                    else:
                        datasorce_queryset_id=None
                    final_data=custom_query_data(row_limit,server_p,server_id,qrset.custom_query,tok1['user_id'],datasorce_queryset_id,srtyp.server_type.upper(),query_name=qrset.query_name,parameter=para,queryset_id=queryset_id)
                    return final_data
                else:
                    if FileDetails.objects.filter(id=file_id).exists():
                        file_db_data=FileDetails.objects.get(id=file_id)
                        file_data=FileType.objects.get(id=file_db_data.file_type)
                    else:
                        return Response({'message':'file_details_id/file_type not exists'},status=status.HTTP_404_NOT_FOUND)
                    if DataSource_querysets.objects.filter(queryset_id=queryset_id).exists():
                        quer_tb=DataSource_querysets.objects.get(queryset_id=queryset_id,file_id=file_id,user_id=tok1['user_id'])
                        datasorce_queryset_id=quer_tb.datasource_querysetid
                    else:
                        datasorce_queryset_id=None
                    final_data=custom_query_data(row_limit,file_p,file_db_data.id,qrset.custom_query,tok1['user_id'],datasorce_queryset_id,file_data.file_type.upper(),query_name=qrset.query_name,parameter=para,queryset_id=queryset_id)
                    return final_data
            else:
                return Response({"message":"Serializer Error"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(tok1,status=tok1['status'])


@api_view(['DELETE'])
def query_delete(request,query_set_id,token):
    if request.method=='DELETE':
        role_list=roles.get_previlage_id(previlage=[previlages.delete_custom_sql])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            if QuerySets.objects.filter(user_id=tok1['user_id'],queryset_id=query_set_id).exists():
                pass
            else:
                return Response({'message':'query_set_id not exists for this user'},status=status.HTTP_404_NOT_FOUND)
            s_id='sample'
            qrst=sheet_data.objects.filter(queryset_id=query_set_id).values('id')
            for sheet_id in qrst:
                # dsdt1234=dashboard_data.objects.get(selected_sheet_ids__contains=str(sheet_id))
                # numbers = [num for num in Connections.litera_eval(dsdt1234.selected_sheet_ids) if num != sheet_id]
                # dashboard_data.objects.filter(id=dsdt1234).update(selected_sheet_ids=numbers)
                dsdt=dashboard_data.objects.filter(user_id=tok1['user_id'],sheet_ids__contains=str(sheet_id)).values()
                Connections.sheet_ds_delete(dsdt,sheet_id,s_id,query_set_id)
            QuerySets.objects.filter(queryset_id=query_set_id).delete()
            DataSource_querysets.objects.filter(queryset_id=query_set_id).delete()
            DataSourceFilter.objects.filter(queryset_id=query_set_id).delete()
            sheet_data.objects.filter(queryset_id=query_set_id).delete()
            SheetFilter_querysets.objects.filter(queryset_id=query_set_id).delete()
            ChartFilters.objects.filter(queryset_id=query_set_id).delete()
            DashboardFilters.objects.filter(queryset_id=query_set_id).delete()
            return Response({'message':'Deleted successfully'},status=status.HTTP_200_OK)
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({'message':'Method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
class query_Name_save(CreateAPIView):
    serializer_class=query_save_serializer

    @transaction.atomic
    def put(self,request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.edit_custom_sql,previlages.create_custom_sql,previlages.view_custom_sql])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                database_id = serializer.validated_data['database_id']
                query_set_id= serializer.validated_data['query_set_id']
                query_name= serializer.validated_data['query_name']
                # custom_query= serializer.validated_data['custom_query']
                file_id= serializer.validated_data['file_id']
                # clean_query_string = re.sub(';', '', custom_query)
                if file_id==None or file_id=='':
                    if ServerDetails.objects.filter(id=database_id,user_id=tok1['user_id']).exists():
                        pass
                    else:
                        return Response({'message':'server id not exists'},status=status.HTTP_404_NOT_FOUND)
                    if QuerySets.objects.filter(user_id=tok1['user_id'],server_id=database_id,queryset_id=query_set_id).exists():
                        if QuerySets.objects.filter(user_id=tok1['user_id'],server_id=database_id,query_name=query_name).exists():
                            return Response({'message':'Query name already exists'},status=status.HTTP_406_NOT_ACCEPTABLE)
                        else:
                            QuerySets.objects.filter(user_id=tok1['user_id'],server_id=database_id,queryset_id=query_set_id).update(query_name=query_name,
                                                                                                                                    updated_at=datetime.datetime.now())
                            return Response({'message':'Query saved successfylly'},status=status.HTTP_200_OK)
                    else:
                        return Response({'message':'Details not found'},status=status.HTTP_404_NOT_FOUND)
                else:
                    if FileDetails.objects.filter(id=file_id).exists():
                        pass
                    else:
                        return Response({'message':'File id not exists'},status=status.HTTP_404_NOT_FOUND)
                    if QuerySets.objects.filter(user_id=tok1['user_id'],file_id=file_id,queryset_id=query_set_id).exists():
                        if QuerySets.objects.filter(user_id=tok1['user_id'],file_id=file_id,query_name=query_name).exists():
                            return Response({'message':'Query name already exists'},status=status.HTTP_406_NOT_ACCEPTABLE)
                        else:
                            QuerySets.objects.filter(user_id=tok1['user_id'],file_id=file_id,queryset_id=query_set_id).update(query_name=query_name,
                                                                                                                                    updated_at=datetime.datetime.now())
                            return Response({'message':'Query saved successfylly'},status=status.HTTP_200_OK)
                    else:
                        return Response({'message':'Details not found'},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message':'Serializer value error'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":tok1['message']},status=status.HTTP_404_NOT_FOUND)
        
    
@api_view(['DELETE'])
@transaction.atomic
def DBDisconnectAPI(request,token,database_id):
    if request.method=='DELETE':
        role_list=roles.get_previlage_id(previlage=[previlages.delete_database])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            if ServerDetails.objects.filter(id=database_id).exists():
                sdt=ServerDetails.objects.get(id=database_id)
                qr_list=QuerySets.objects.filter(server_id=sdt.id).values()
                for qr_id in qr_list:
                    sh_dt=sheet_data.objects.filter(queryset_id=qr_id['queryset_id']).values()
                    for qr in sh_dt:
                        dsdt=dashboard_data.objects.filter(sheet_ids__contains=str(qr['id'])).values()
                        Connections.sheet_ds_delete(dsdt,qr['id'],sdt.id,qr_id['queryset_id'])
                    QuerySets.objects.filter(queryset_id=qr_id['queryset_id']).delete()
                    DataSource_querysets.objects.filter(queryset_id=qr_id['queryset_id']).delete()
                    DataSourceFilter.objects.filter(queryset_id=qr_id['queryset_id']).delete()
                    sheet_data.objects.filter(queryset_id=qr_id['queryset_id']).delete()
                    SheetFilter_querysets.objects.filter(queryset_id=qr_id['queryset_id']).delete()
                    ChartFilters.objects.filter(queryset_id=qr_id['queryset_id']).delete()
                    DashboardFilters.objects.filter(queryset_id=qr_id['queryset_id']).delete()
                ServerDetails.objects.get(id=database_id).delete()
                return Response({'message':'Database Deleted Successful'},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Invalid Database ID"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({'message':'Method Not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

class GetServerTablesList(CreateAPIView):
    serializer_class = SearchFilterSerializer
    
    def post(self, request,token,database_id):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            
            # Search Filter Only works on Display Name Column in Server Details
            search_table_name = serializer.validated_data['search']
            querySetId = serializer.validated_data['querySetId']
            tok1 = test_token(token)
            if tok1['status'] == 200:
                if querySetId==None or querySetId=='':
                    queryset_name=None
                else:
                    if QuerySets.objects.filter(queryset_id=querySetId,user_id=tok1['user_id']).exists():
                        qrtb=QuerySets.objects.get(queryset_id=querySetId)
                        queryset_name=qrtb.query_name
                    else:
                        return Response({'message':'queryset not exists'},status=status.HTTP_404_NOT_FOUND)
                    
                if ServerDetails.objects.filter(id=database_id).exists():
                    sd = ServerDetails.objects.get(id=database_id)
                    st = ServerType.objects.get(id=sd.server_type)
                    server_conn=server_connection(sd.username,sd.password,sd.database,sd.hostname,sd.port,sd.service_name,st.server_type.upper(),sd.database_path)
                    if server_conn['status']==200:
                        engine=server_conn['engine']
                        cursor=server_conn['cursor']
                    else:
                        return Response(server_conn,status=server_conn['status'])

                    if st.server_type.upper()=="POSTGRESQL" or st.server_type =='MYSQL' or st.server_type=="SQLITE":
                        inspector = inspect(engine)
                        schemas = inspector.get_schema_names()
                        result = {"schemas": []}
                        for i in schemas:
                            if i != 'information_schema':
                                ll = []
                                table_names = inspector.get_table_names(schema=i)
                                table_names_sorted = sorted(table_names)
                                
                                if search_table_name == '' or search_table_name == ' ' or search_table_name == None :
                                    for table_name in table_names_sorted:
                                        columns = inspector.get_columns(table_name, schema=i)
                                        cols = [{"column": column['name'].lower(), "datatype": str(column['type']).lower()} for column in columns]
                                        ll.append({"schema":i,"table":table_name,"columns":cols})
                                else:
                                    filter_table_names = [table_name for table_name in table_names if '{}'.format(search_table_name) in table_name.lower()]
                                    for table in filter_table_names:
                                        columns = inspector.get_columns(table, schema=i)
                                        cols = [{"column": column['name'].lower(), "datatype": str(column['type']).lower()} for column in columns]
                                        ll.append({"schema":i,"table":table,"columns":cols})
                                if ll ==[] :
                                    pass
                                else:
                                    result["schemas"].append({"schema": i, "tables": ll})
                        return Response(
                            {
                                "message": "Successfully Connected to DB",
                                "queryset_name":queryset_name,
                                "data": result,
                                'display_name': sd.display_name,
                                "database": {
                                    "database_id": sd.id,
                                    "server_type": st.server_type,
                                    "hostname": sd.hostname,
                                    "database": sd.database,
                                    "port": sd.port,
                                    "username": sd.username,
                                    "service_name": sd.service_name,
                                    "display_name": sd.display_name,
                                }
                            }, status=status.HTTP_200_OK)
                    elif st.server_type.upper()=="ORACLE":
                        inspector = inspect(engine)
                        
                        # Get Specific Schema Based Tables
                        table_names = inspector.get_table_names(schema=sd.username)
                        table_names_sorted = sorted(table_names)
                        
                        ll=[]
                        if search_table_name == '' or search_table_name == ' ' or search_table_name == None :
                            for table_name in table_names_sorted:
                                columns = inspector.get_columns(table_name, schema=sd.username)
                                cols = [{"column": column['name'].lower(), "datatype": str(column['type']).lower()} for column in columns]
                                ll.append({"schema":sd.username,"table":table_name,"columns":cols})
                        else:
                            filter_table_names = [table_name for table_name in table_names if '{}'.format(search_table_name) in table_name.lower()]
                            for table in filter_table_names:
                                columns = inspector.get_columns(table, schema=sd.username)
                                cols = [{"column": column['name'].lower(), "datatype": str(column['type']).lower()} for column in columns]
                                ll.append({"schema":sd.username,"table":table,"columns":cols})
                        if ll ==[] :
                            pass
                        else:
                            result = {"schemas": [{"schema": sd.username, "tables": ll}]}
                        
                        return Response(
                            {
                                "message": "Successfully Connected to DB",
                                "queryset_name":queryset_name,
                                "data": result,
                                'display_name': sd.display_name,
                                "database": {
                                    "database_id":sd.id,
                                    "server_type":st.server_type,
                                    "hostname":sd.hostname,
                                    "database":sd.database,
                                    "port" :sd.port,
                                    "username":sd.username,
                                    "service_name":sd.service_name,
                                    "display_name":sd.display_name,
                                }
                            }, status=status.HTTP_200_OK)
                    elif st.server_type.upper()=="MONGODB":
                        db=engine
                        final_list={}
                        colms=[]
                        final_ls=[]
                        collections = db.list_collection_names()
                        for collection_name in collections:
                            final_list['schema']=None
                            final_list['table']=collection_name
                            collection = db[collection_name]
                            documents = collection.find()
                            for field in documents:
                                cllist=[]
                                colms.append({'columns':cllist.append(field),'datatypes':None})
                            final_list['columns']=colms
                        final_ls.append(final_list)
                        result = {"schemas": [{"schema": None, "tables": final_ls}]}
                        return Response(
                            {
                                "message": "Successfully Connected to DB",
                                "queryset_name":queryset_name,
                                "data": result,
                                'display_name': sd.display_name,
                                "database": {
                                    "database_id":sd.id,
                                    "server_type":st.server_type,
                                    "hostname":sd.hostname,
                                    "database":sd.database,
                                    "port" :sd.port,
                                    "username":sd.username,
                                    "service_name":sd.service_name,
                                    "display_name":sd.display_name,
                                }
                            }, status=status.HTTP_200_OK)
                    elif st.server_type.upper()=="MICROSOFTSQLSERVER":
                        tables_query = """
                        SELECT 
                            TABLE_SCHEMA,
                            TABLE_NAME
                        FROM 
                            INFORMATION_SCHEMA.TABLES
                        WHERE 
                            TABLE_TYPE = 'BASE TABLE'
                        ORDER BY 
                            TABLE_SCHEMA, TABLE_NAME
                        """
                        cursor.execute(tables_query)
                        tables = cursor.fetchall()
                        schema_info = {}
                        for table in tables:
                            schema = table.TABLE_SCHEMA
                            table_name = table.TABLE_NAME
                            if schema not in schema_info:
                                schema_info[schema] = {}
                            columns_query = f"""
                            SELECT 
                                COLUMN_NAME,
                                DATA_TYPE
                            FROM 
                                INFORMATION_SCHEMA.COLUMNS
                            WHERE 
                                TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table_name}'
                            ORDER BY 
                                ORDINAL_POSITION
                            """
                            cursor.execute(columns_query)
                            columns = cursor.fetchall()
                            schema_info[schema][table_name] = [(column.COLUMN_NAME, column.DATA_TYPE) for column in columns]
                        formatted_data = []
                        for schema_name, tables in schema_info.items():
                            schema_entry = {"schema": schema_name, "tables": []}
                            for table_name, columns in tables.items():
                                table_entry = {"schema": schema_name, "table": table_name, "columns": []}
                                for column_name, data_type in columns:
                                    column_entry = {"column": column_name, "datatype": data_type}
                                    table_entry["columns"].append(column_entry)
                                schema_entry["tables"].append(table_entry)
                            formatted_data.append(schema_entry)
                        result12 = {"schemas":formatted_data}
                        return Response(
                            {
                                "message":"Successfully Connected to DB",
                                "queryset_name":queryset_name,
                                "data":result12,
                                'display_name':sd.display_name,
                                "database":
                                    {
                                        "database_id":sd.id,
                                        "database_name":sd.database
                                    }
                                }
                            ,status=status.HTTP_200_OK)
                    elif st.server_type.upper()=="SNOWFLAKE":
                        inspector = inspect(engine)
                        schemas = inspector.get_schema_names()
                        schema_info = []
                        for schema in schemas:
                            tables = inspector.get_table_names(schema=schema)
                            tables_info = []
                            table_names_sorted = sorted(tables)
                            for table in table_names_sorted:
                                columns = inspector.get_columns(table, schema=schema)
                                columns_info = [{'column': col['name'], 'datatype': str(col['type'])} for col in columns]
                                tables_info.append({
                                    "schema": schema,
                                    "table": table,
                                    "columns": columns_info
                                })
                            schema_info.append({
                                "schema": schema,
                                "tables": tables_info
                            })
                        return Response(
                            {
                                "message":"Successfully Connected to DB",
                                "queryset_name":queryset_name,
                                "data":{'schemas':schema_info},
                                'display_name':sd.display_name,
                                "database":
                                    {
                                        "database_id":sd.id,
                                        "database_name":sd.database
                                    }
                                }
                            ,status=status.HTTP_200_OK)
                    else:
                        return Response({'message':"server not exists"},status=status.HTTP_404_NOT_FOUND)  
                else:
                    return Response({'message':"Invalid Data Base ID"},status=status.HTTP_404_NOT_FOUND)                           
            else:
                return Response(tok1,status=tok1['status'])
