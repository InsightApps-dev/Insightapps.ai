
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import psycopg2,cx_Oracle
from dashboard import models,serializers,views,roles,previlages,files
import pandas as pd
from sqlalchemy import text,inspect
import numpy as np
from .models import ServerDetails,ServerType,QuerySets
import ast,re,itertools
import datetime
import boto3,pyodbc
import json
import requests
from project import settings
import io
import sqlite3
import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Float, Date, Time, DateTime, Numeric,TIMESTAMP,VARCHAR,BIGINT,SMALLINT,CHAR,Text,TEXT,VARBINARY
import pprint
from collections import defaultdict
from pymongo import MongoClient
from urllib.parse import quote_plus
from urllib.parse import quote



def server_connection(username, password, database, hostname,port,service_name,parameter,server_path):
    password1234=views.decode_string(password)
    try:
        if parameter=="POSTGRESQL":
            url = "postgresql://{}:{}@{}:{}/{}".format(username,password1234,hostname,port,database)
        elif parameter=="ORACLE":
            url = 'oracle+cx_oracle://{}:{}@{}:{}/{}'.format(username,password1234,hostname,port,service_name)
        elif parameter=="MYSQL":
            url = f'mysql+mysqlconnector://{username}:{password1234}@{hostname}:{port}/{database}'
        elif parameter=="SNOWFLAKE":
            encoded_password = quote(password1234)
            url = f'snowflake://{username}:{encoded_password}@{hostname}/{database}?port={port}'
        elif parameter=="IBMDB2":
            url = f'ibm_db_sa://{username}:{password1234}@{hostname}:{port}/{database}'
        elif parameter=="MICROSOFTSQLSERVER":
            driver='ODBC Driver 17 for SQL Server'
            connection_string = f'DRIVER={driver};SERVER={hostname};DATABASE={database};Trusted_Connection=yes;'
            conn = pyodbc.connect(connection_string)
        elif parameter=="MICROSOFTACCESS" or parameter=="SQLITE":
            sq_msacces=server_path_function(server_path,parameter)
            if sq_msacces['status']==200:
                url = sq_msacces['url']
            else:
                return sq_msacces
        elif parameter=="SYBASE":
            url = f'sybase+pyodbc://{username}:{password1234}@{hostname}:{port}/{database}'
        elif parameter=="MONGODB":
            mongo=mongo_db(username, password, database, hostname,port)
            return mongo
            

        # engine = create_engine(url, echo=True)
        if parameter=="MICROSOFTSQLSERVER": 
            engine = conn
            cursor = conn.cursor()
        else:
            engine = create_engine(url)
            cursor = engine.connect()

        data={
            "status":200,
            "engine":engine,
            "cursor":cursor
        }
        return data
    except Exception as e:
        data={
            "status":400,
            "message" : f"{e}"
        }
        return data



def mongo_db(username, password, database, hostname, port):
    try:
        if username=='' or None and password =='' or None:
            client = MongoClient(hostname, int(port))
        else:
            connection_string = f'mongodb://{username}:{password}@{hostname}:{int(port)}/{database}'
            client = MongoClient(connection_string)
        
        db = client[database]
        data = {
            "status":200,
            "engine":db,
            "cursor":None
        }
        return data
    except Exception as e:
        data={
            "status":400,
            "message" : f"{e}"
        }
        return data
    

def server_path_function(server_path,parameter):
    if server_path==None or server_path=='':
        data = {
            "status":406,
            "message":"database_path is mandatory"
        }
        return data
    else:
        if parameter=="MICROSOFTACCESS":
            # database_path = r'C:\path\to\your\database.accdb'
            url = f'access+pyodbc:///?Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={str(server_path)}'
        elif parameter=="SQLITE":
            # database_path = 'path/to/your/database.db'
            url = f'sqlite:///{str(server_path)}'
        data = {
            "status":200,
            "url":url
        }
        return data


    
def get_sqlalchemy_type(type_code):
    type_code_map = {
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
    # Add other type codes as needed
}
    value =type_code_map.get(type_code, String)()
    return value

def read_excel_file_data(file_path,filename):
    try:
        encoded_url = quote(file_path, safe=':/')
        xls = pd.ExcelFile(encoded_url)
        l=[]
        sheet_name = []
        for i in xls.sheet_names:
            sheet_name.append(i)
            data_csv = pd.read_excel(xls,sheet_name=i)
            data_csv = data_csv.fillna(value='NA')
            url =f'sqlite:///columns.db'
            engine = create_engine(url)
            for column in data_csv.columns:
                if data_csv[column].dtype == 'object':
                    data_csv[column] = data_csv[column].astype(str)  # Convert to TEXT
                elif data_csv[column].dtype == 'int64':
                    data_csv[column] = data_csv[column].astype(int)  # Convert to INTEGER
                elif data_csv[column].dtype == 'float64':
                    data_csv[column] = data_csv[column].astype(float)
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


def read_csv_file_data(file_path,filename):
    try:
        df = pd.read_csv(file_path)
        df = df.fillna(value='NA')
        url =f'sqlite:///columns.db'
        engine = create_engine(url)
        df.to_sql(filename, engine, index=False, if_exists='replace')
        f_dt = {
                "status":200,
                "engine":engine,
                "cursor":engine.connect(),
                "tables_names":filename
            }
        return f_dt
    except Exception as e:
        f_dt = {
            "status":400,
            "message":e
        }
        return f_dt
    

def delete_tables_sqlite(cur,engine,tables):
    # if len(tables)>0:
    #     for table1 in tables:
    #         drop_table_sql = f'DROP TABLE IF EXISTS \"{table1}\";'
    #         a= cur.execute(text(drop_table_sql))
    #         cur.commit()
    #         print(a)
    #         # engine.commit()
    try:
        with cur as connection:
            if len(tables) > 0:
                for table in tables:
                    drop_table_sql = text(f'DROP TABLE IF EXISTS \"{table}\";')
                    connection.execute(drop_table_sql)
            connection.commit()
    except Exception as e:
        print(e)

    
def file_details(file_type,file_data):
    if file_type is not None or  file_data !='' or file_data is not  None or file_data !='':
        pattern = r'/insightapps/(.*)'
        match = re.search(pattern, str(file_data.source))
        filename = match.group(1)
        file,fileext = filename.split('.')
        file_url = file_data.source
        if (file_type.upper()=='EXCEL' and fileext == 'xlsx') or (file_type.upper()=='EXCEL' and fileext == 'xls'):
            read_data = read_excel_file_data(file_url,file)
        elif  file_type.upper()=='CSV' and fileext == 'csv':
            read_data = read_csv_file_data(file_url,file)
        else:
            return 'Nodata'

        if read_data['status'] ==200:
            data = {
                'status':200,
                'engine':read_data['engine'],
                'cursor':read_data['cursor'],
                'tables_names':read_data['tables_names']
            } 
        else:
            data = {
                'status':read_data['status'],
                'message':read_data
            }
        return data
    else:
        data = {
            'status':400,
            'message':'no Data'
        }
        return data 
    


def classify_columns(names, type):
    types=[str(col).replace("()", '').lower() for col in type]
    dimension_types = ['String','string','Date', 'TIMESTAMP', 'Boolean', 'Time', 'datetime','varchar','bp char','text','varchar2','NVchar2','long','char','Nchar','character varying','date','time','datetime','timestamp','timestamp with time zone','timestamp without time zone','timezone','time zone','bool','boolean']
    measure_types = ['Integer', 'Float', 'Numeric', 'int', 'float','numeric','float','number','double precision','smallint','integer','bigint','decimal','numeric','real','smallserial','serial','bigserial','binary_float','binary_double']
    dimensions = []
    measures = []
    for name, dtype in zip(names, types):
        if dtype in dimension_types:
            dimensions.append({"column":name,"data_type":str(dtype)})
        elif dtype in measure_types:
            measures.append({"column":name,"data_type":str(dtype)})
    return dimensions, measures


def snowflake_data(query):
    table_pattern = re.compile(
        r'FROM\s+([\w\d]+)\.([\w\d]+)\s+AS\s+"([\w\d_]+)"'  # Match FROM clause with schema, table, alias
        r'|JOIN\s+([\w\d]+)\.([\w\d]+)\s+AS\s+"([\w\d_]+)"',  # Match JOIN clause with schema, table, alias
        re.IGNORECASE
    )
    column_pattern = re.compile(
        # r'"(\w+)"\.(\w+)\s+AS\s+"(\w+)"',  # Match column with alias
        r'"([\w\d_]+)"\.(\w+)\s+AS\s+"(\w+)"',  # Match column with alias
        re.IGNORECASE
    )
    table_matches = table_pattern.findall(query)
    tables_info = {}
    for match in table_matches:
        if match[0]:  # FROM clause matched
            schema_name, table_name, table_alias = match[0], match[1], match[2]
        else:  # JOIN clause matched
            schema_name, table_name, table_alias = match[3], match[4], match[5]
        if not table_alias:
            table_alias = table_name
        tables_info[table_alias] = (schema_name, table_name)
    op = re.sub(r'\(.*?\)', '', query)
    column_matches = column_pattern.findall(op)
    columns_info = []
    for match in column_matches:
        table_alias, column_name, column_alias = match[0], match[1], match[2]
        schema_name, table_name = tables_info.get(table_alias, (None, None))
        columns_info.append({
            "schema": schema_name,
            "table_name": table_name,
            "table_alias": table_alias,
            "column_name": column_name,
            "column_alias": column_alias
        })
    return columns_info


def query_filter(sql_query,server_type):
    if server_type=="SNOWFLAKE":
        snowflake=snowflake_data(str(sql_query))
        return snowflake
    else:
        table_pattern = re.compile(r'FROM\s+"([^"]+)"\."([^"]+)"\s+("([^"]+)")?|JOIN\s+"([^"]+)"\."([^"]+)"\s+("([^"]+)")?', re.IGNORECASE)
        table_matches = table_pattern.findall(str(sql_query))
        tables_info = {}
        for match in table_matches:
            if match[0]:
                schema_name, table_name, _, table_alias = match[0], match[1], match[2], match[3]
            else:
                schema_name, table_name, _, table_alias = match[4], match[5], match[6], match[7]
            tables_info[table_alias] = (schema_name, table_name)
        column_pattern = re.compile(r'"([^"]+)"\."([^"]+)"\s+as\s+"([^"]+)"', re.IGNORECASE)
        column_matches = column_pattern.findall(str(sql_query))

        columns_info = []
        for table_alias, column_name, column_alias in column_matches:
            schema_name, table_name = tables_info.get(table_alias, ('public', table_alias))
            columns_info.append({
                "schema": schema_name,
                "table_name": table_name,
                "table_alias": table_alias,
                "column_name": column_name,
                "column_alias": column_alias
            })
        return columns_info


def custom_sql(cursor,type_codes,column_list,ser_db_data,server_details_id,queryset_id,data_types,parameter):
    if parameter=="file":
        server_id=None
        file_id=server_details_id
    else:
        server_id=server_details_id
        file_id=None
    if data_types==None or data_types=='':
        dt_list=[]
        for i in type_codes:
            a1=get_sqlalchemy_type(i) 
            dt_list.append(a1)
        dt_list=dt_list
    else:
        dt_list=data_types
    dimensions,measures=classify_columns(column_list,dt_list)
    fl_data=[]
    data = {
        "database_name":ser_db_data.display_name,
        "server_id":server_id,
        "file_id":file_id,
        "queryset_id":queryset_id,
        "schema":"",
        "table_name":"Custom_query",
        "table_alias":"Custom_query",
        "dimensions":dimensions,
        "measures":measures,
    }
    fl_data.append(data)
    return Response(fl_data,status=status.HTTP_200_OK)

def joining_sql(cursor,type_codes,engine,quer_tb,queryset_id,server_id,ser_db_data,server_type,data_types,parameter):
    if parameter=="file":
        server_id1=None
        file_id=server_id
    else:
        server_id1=server_id
        file_id=None
    if data_types==None or data_types=='':
        dt_list=[]
        for i in type_codes:
            a1=get_sqlalchemy_type(i) 
            dt_list.append(a1)
        dt_list=dt_list
    else:
        dt_list=data_types
    if server_type=="MICROSOFTSQLSERVER":
        clea_qr=str(quer_tb.custom_query).replace('[','"').replace(']','"')
        query1 = "{}".format(clea_qr)
        qr_flter=query_filter(query1,server_type)
    elif server_type=="MYSQL":
        clea_qr=str(quer_tb.custom_query).replace('`','"')
        qr_flter=query_filter(text(clea_qr),server_type)
    else:
        qr_flter=query_filter(text(quer_tb.custom_query),server_type)
    if len(dt_list) < len(qr_flter):
        dt_list += [None] * (len(qr_flter) - len(dt_list))   ## adding null for no datatype
    for clmn, dt_tp in zip(qr_flter, dt_list):
        clmn['data_type'] = dt_tp    ## adding column wise datatypes
    tables_dict = {}
    for item in qr_flter:
        table_alias = item['table_alias']
        table_name = item['table_name']
        if table_alias not in tables_dict:
            tables_dict[table_alias] = {
                'schema': item['schema'],
                'table_name': table_name,
                'table_alias': table_alias,
                'columns': [],
                'dimensions':[],
                'measures':[]
            }
        column_info = {
            'column': item['column_alias'],
            'data_type': item['data_type']
        }
        tables_dict[table_alias]['columns'].append(column_info) # adding table wise columns,datatypes to existing data
    res1=list(tables_dict.items())
    def fetch_columns(table_alias):
        for table_tuple in res1:
            if table_tuple[0] == table_alias:
                return table_tuple[1]['columns']
        return None
    for table_index, (table_alias, table_data) in enumerate(res1):
        user_columns = fetch_columns(str(res1[table_index][1]['table_alias'])) # to fetch table wise columns,datatypes
        cls1=[]
        dts1=[]
        for i in user_columns:
            cls1.append(i['column'])
            dts1.append(i['data_type'])
        dimensions,measures=classify_columns(cls1,dts1)
        del res1[table_index][1]['columns']  # Remove the 'columns' key from the table data
        res1[table_index][1]['dimensions'] = dimensions
        res1[table_index][1]['measures'] = measures
        res1[table_index][1]['database_name'] = ser_db_data.display_name
        res1[table_index][1]['server_id'] = server_id1
        res1[table_index][1]['file_id'] = file_id
        res1[table_index][1]['queryset_id'] = queryset_id
        cls1.clear()
        dts1.clear()
    flat_filters_data = [item for sublist in res1 for item in sublist] # to remove extra list
    cleaned_data = [item for item in flat_filters_data if isinstance(item, dict)] # to remove the data other than in dict
    if server_type=="SNOWFLAKE":
        cleaned_data=cleaned_data
    else:
        cleaned_data=cleaned_data[:-1]
    return Response(cleaned_data,status=status.HTTP_200_OK)


def mongo_db_data(engine,display_name,server_id,queryset_id):
    db=engine
    final_list={}
    colms=[]
    final_ls=[]
    collections = db.list_collection_names()
    for collection_name in collections:
        final_list['schema']=None
        final_list['table_name']=collection_name
        final_list['table_alias']=collection_name
        collection = db[collection_name]
        documents = collection.find()
        for field in documents:
            data = {
                'column':field,
                'data_type':None
            }
            # colms.append({'column':field,'data_type':None})
            colms.append(data)
            final_list['dimensions']=colms
            final_list['measures']=[]
            final_list['database_name']=display_name
            final_list['server_id']=server_id
            final_list['queryset_id']=queryset_id
    final_ls.append(final_list)
    return final_ls


#### Columns extraction from table
class new_column_extraction(CreateAPIView):
    serializer_class=serializers.new_table_input

    def post(self,request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.create_sheet,previlages.view_sheet,previlages.edit_sheet])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            serializer=self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):  
                server_details_id=serializer.validated_data['db_id']
                queryset_id=serializer.validated_data['queryset_id']
                file_id=serializer.validated_data['file_id']
                if server_details_id==None or server_details_id=='':
                    try:
                        file_db_data=models.FileDetails.objects.get(id=file_id)
                        file_data=models.FileType.objects.get(id=file_db_data.file_type)
                    except:
                        return Response({'message':'file_details_id/file_type not exists'},status=status.HTTP_404_NOT_FOUND)
                    try:
                        quer_tb=models.QuerySets.objects.get(queryset_id=queryset_id,file_id=file_id,user_id=tok1['user_id'])
                    except:
                        return Response({'message':'Queryset id not matching with the user files details'},status=status.HTTP_406_NOT_ACCEPTABLE)
                elif file_id==None or file_id=='':
                    try:
                        ser_db_data=models.ServerDetails.objects.get(id=server_details_id,is_connected=True)
                        ser_data=models.ServerType.objects.get(id=ser_db_data.server_type)
                    except:
                        return Response({'message':'server_details_id/server_type not exists'},status=status.HTTP_404_NOT_FOUND)
                    try:
                        quer_tb=models.QuerySets.objects.get(queryset_id=queryset_id,server_id=server_details_id,user_id=tok1['user_id'])
                    except:
                        return Response({'message':'Queryset id not matching with the user server details'},status=status.HTTP_406_NOT_ACCEPTABLE)
    
                if server_details_id==None or server_details_id=='':
                    files_data = file_details(file_data.file_type,file_db_data)
                    if files_data['status']==200:
                        engine=files_data['engine']
                        cursor=files_data['cursor']
                        result=cursor.execute(text(quer_tb.custom_query))
                        codes=result.cursor.description
                        type_codes = [column[1] for column in codes]
                        column_list = [column[0] for column in codes]
                        data_types=None
                    else:
                        return Response({"message":files_data['message']},status=files_data['status'])
                    if quer_tb.is_custom_sql==True:
                        custom=custom_sql(cursor,type_codes,column_list,file_db_data,file_id,queryset_id,data_types,parameter="file")
                        delete_tables_sqlite(cursor,engine,files_data['tables_names'])
                        return custom
                    else:
                        joining=joining_sql(cursor,type_codes,engine,quer_tb,queryset_id,file_id,file_db_data,file_data.file_type.upper(),data_types,parameter="file")
                        delete_tables_sqlite(cursor,engine,files_data['tables_names'])
                        return joining
                elif file_id==None or file_id=='':
                    connect1=server_connection(ser_db_data.username,ser_db_data.password,ser_db_data.database,ser_db_data.hostname,ser_db_data.port,ser_db_data.service_name,ser_data.server_type.upper(),ser_db_data.database_path)
                    if connect1['status']==200:
                        engine=connect1['engine']
                        cursor=connect1['cursor']
                        if ser_data.server_type.upper()=="MONGODB":
                            mongo=mongo_db_data(engine,ser_db_data.display_name,server_details_id,queryset_id)
                            return mongo
                        else:
                            if ser_data.server_type.upper()=="MICROSOFTSQLSERVER":
                                query = "{}".format(quer_tb.custom_query)
                                result = cursor.execute(query)
                                codes = cursor.description
                                column_list = [column[0] for column in codes]
                                type_codes = [column[1] for column in codes]
                                data_types = [data_type[1].__name__ for data_type in codes]
                            else:
                                result=cursor.execute(text(quer_tb.custom_query))
                                codes=result.cursor.description
                                type_codes = [column[1] for column in codes]
                                column_list = [column[0] for column in codes]
                                data_types=None
                    else:
                        return Response({"message":connect1['message']},status=connect1['status'])
                    if quer_tb.is_custom_sql==True:
                        custom=custom_sql(cursor,type_codes,column_list,ser_db_data,server_details_id,queryset_id,data_types,parameter="server")
                        return custom
                    else:
                        joining=joining_sql(cursor,type_codes,engine,quer_tb,queryset_id,server_details_id,ser_db_data,ser_data.server_type.upper(),data_types,parameter="server")
                        return joining
                else:
                    return Response({'message':'not acceptable'},status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({'message':'serializer value error'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(tok1,status=tok1['status'])