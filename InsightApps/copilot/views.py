from dashboard.columns_extract import server_connection
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from sqlalchemy import text
from dashboard.models import QuerySets, ServerDetails, ServerType
from .serializers import ChartCopilot,APIKEYServerialzer
from dashboard.Connections import table_name_from_query
import ast
import base64
import json
import requests
import re
import os 
import subprocess
# import api_key


# api_key

# # Get the value of the environment variable
# my_var_value = os.environ.get('OPENAI_API_KEY')

# # Check the value of OPENAI_API_KEY using a command
# if os.name == 'nt':  # For Windows
#     result = subprocess.run(['echo', '%OPENAI_API_KEY%'], shell=True, capture_output=True, text=True)
# else:  # For Unix-based systems (Linux, macOS)
#     result = subprocess.run(['printenv', 'OPENAI_API_KEY'], capture_output=True, text=True)


# API_KEY = result.stdout.strip() or result.stdout
def create_default_api_key_file():
    json_file_path = 'paths/api_key.json'  # Replace with the correct path if needed

    # Check if the file already exists
    if not os.path.isfile(json_file_path):
        # File does not exist, create it and write default content
        with open(json_file_path, 'w') as file:
            default_data = {"API_KEY": ""}
            json.dump(default_data, file, indent=4)
        print(f'File {json_file_path} created with default content.')
    else:
        pass
        print(f'File {json_file_path} already exists.')
def get_api_key_from_file():
    json_file_path = 'paths/api_key.json'  # Replace with the correct path

    with open(json_file_path, 'r') as file:
        data = json.load(file)
        return data.get('API_KEY')
    
# Create the file with default content if it does not exist
create_default_api_key_file()


# Create your views here.
def validate_api_key(KEY):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {KEY}"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{'role': 'user', 'content':"Say this is a test"}]
            # 'max_tokens':5
        }
    )
    if response.status_code == 200:
        return Response({'message': True}, status=status.HTTP_200_OK)
    elif response.status_code == 404:
        res = {'error': {'message': 'The model `gpt-3.5-turb` does not exist or you do not have access to it.', 'type': 'invalid_request_error', 'param': None, 'code': 'model_not_found'}}
        return Response({'message': res['error']['message']}, status=status.HTTP_404_NOT_FOUND)
        
    elif response.status_code == 401:
        # res = {'error': {'message': 'Incorrect API key provided: "{KEY}". You can find your API key at https://platform.openai.com/account/api-keys.'.format(KEY), 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}
        return Response({'message': f"Incorrect API key provided: '{KEY}'. \n\n You can find your API key at https://platform.openai.com/account/api-keys."}, status=status.HTTP_401_UNAUTHORIZED)
    
class ValidateApiKeyView(CreateAPIView):
    serializer_class = APIKEYServerialzer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            api_key = serializer.validated_data['key']
            validation_response = validate_api_key(api_key)

            if validation_response.status_code == 200:
                with open('paths/api_key.json', 'w') as f:
                    json.dump({'API_KEY': api_key}, f)
                return Response({'message': True}, status=status.HTTP_200_OK)
            
            return validation_response
    
class GetServerTablesList(CreateAPIView):
    serializer_class = ChartCopilot
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            query_set_id = serializer.validated_data['id']
            user_prompt = serializer.validated_data['prompt']
            API_KEY = get_api_key_from_file()
            a = validate_api_key(API_KEY)
            
            if a.status_code ==200:
                pass
            elif a.status_code == 401:
                return Response({'message': a.data}, status=status.HTTP_401_UNAUTHORIZED)
            elif a.status_code == 404:
                return Response({'message':a.data},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message':"Please try again"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            if not QuerySets.objects.filter(queryset_id=query_set_id).exists():
                return Response({'message': "Invalid QuerySet ID"}, status=status.HTTP_404_NOT_FOUND)
            
            if QuerySets.objects.filter(queryset_id=query_set_id,is_custom_sql=True).exists():
                return Response({'message': "Chart Suggestions on Custom Query, NOT IMPLEMENTED"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            qs = QuerySets.objects.get(queryset_id=query_set_id)
            sd = ServerDetails.objects.get(id=qs.server_id)
            server_type = ServerType.objects.get(id=sd.server_type).server_type
            
            server_conn =server_connection(sd.username,sd.password,sd.database,sd.hostname,sd.port,sd.service_name,server_type.upper(),sd.database_path)
            if server_conn['status'] != 200:
                return Response(server_conn, status=server_conn['status'])
            
            engine = server_conn['engine']
            cursor = server_conn['cursor']
            db_type = server_type
            
            # d = fetch_tables_from_query(qs)
            # tables = d['tables']
            
            # Create a list to store the results in schema.table_name format
            tables_list = qs.table_names
            tables_list = ast.literal_eval(tables_list)
            tables = []

            # Iterate through the list
            for entry in tables_list:
                if len(entry) == 2:
                    schema, table = entry
                elif len(entry) == 3:
                    schema, table, _ = entry  # Ignore the alias part
                else:
                    continue  # Skip entries that don't match the expected structure
                tables.append(f"{schema}.{table}")
            result = get_table_meta_data(engine, cursor, tables, db_type)
            # Ensure `result['data']` is a string that can be parsed by `ast.literal_eval`
            if isinstance(result, dict) and 'data' in result:
                result_data_str = json.dumps(result['data'])
                op = ast.literal_eval(result_data_str)
            else:
                return Response({"message": "Error fetching table metadata."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            if can_build_chart(op, user_prompt) != "YES":
                return Response({
                    "data": "The question <b>{}</b> doesn't seem to match any of the keywords in the provided table metadata. <br><br>Could you please rephrase the question and ask again ?".format(user_prompt)
                })
            
            # Initial attempt to correct the format
            formatted_data = correct_format(op)
            
            if formatted_data['status'] == "error":
                # Retry getting GPT chart suggestions if correct_format fails
                final_res = get_gpt_chart_suggestions(op, user_prompt)
                if 'error' in final_res:
                    return Response({"message": final_res['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # Try to correct the format again with new suggestions
                text = final_res['choices'][0]['message']['content']
                data = json.loads(text)
                formatted_data = correct_format(data)
                if formatted_data['status'] == "error":
                    return Response({"message": "Error generating chart suggestions. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    data = formatted_data['data']
            else:
                data = formatted_data['data']
            
            # column_type_map = map_columns_to_datatypes(op)
            # corrected_charts = validate_chart_data(data, column_type_map)
                
            final_data = []
            for chart in data['charts']:
                chart_type_lower = chart['chart_type'].lower()
                
                # Determine chart_id based on chart_type
                if "bar" in chart_type_lower:
                    chart_id = 6
                elif "line" in chart_type_lower:
                    chart_id = 13
                elif "pie" in chart_type_lower:
                    chart_id = 24
                elif "area" in chart_type_lower:
                    chart_id = 17
                else:
                    chart_id = 1
                    
                new_data = {
                    "chart_title": chart['chart_title'],
                    "chart_type": chart['chart_type'],
                    "database_id": qs.server_id,
                    "queryset_id": qs.queryset_id,
                    "col": chart['col'],
                    "row": chart['row'],
                    "filter_id": [],
                    "columns": [
                        {
                            "column": col[0],
                            "type": col[1]
                        } for col in chart['col']
                    ],
                    "rows": [
                        {
                            "column": row[0],
                            "type": row[2]
                        } for row in chart['row']
                    ],
                    "datasource_quertsetid": "",
                    "sheetfilter_querysets_id": "",
                    "chart_id":chart_id
                }
                final_data.append(new_data)
            return Response({"data": final_data})
        else:
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


def correct_format(data):
    try:
        for chart in data['charts']:
            for row in chart['row']:
                if len(row) == 3 and row[1] in ["avg", "sum", "min", "max", "count"] and row[2] == "":
                    row[1], row[2] = "aggregate", row[1]
                elif len(row) == 2 and row[1] in ["avg", "sum", "min", "max", "count"]:
                    row.append(row[1])
                    row[1] = "aggregate"
        return {"status": "success", "data": data}
    except Exception:
        return {"status": "error"}
    
def decode_string(encoded_string):
    # Add padding if necessary
    padding_needed = len(encoded_string) % 4
    if padding_needed:
        encoded_string += '=' * (4 - padding_needed)
    
    try:
        # Decode the Base64 string
        decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
        return decoded_bytes.decode('utf-8')
    except (base64.binascii.Error, UnicodeDecodeError) as e:
        # Handle errors if decoding fails
        print(f"Decoding error: {e}")
        return str(e)

def fetch_tables_from_query(query):
    try:
        return table_name_from_query(query)
    except Exception as e:
        return str(e)

def get_table_meta_data(engine, cursor, tables_list, database_type, mongo_client=None):
    try:
        if database_type == 'SQLITE':
            tables = [entry.split('.')[1] if '.' in entry else entry for entry in tables_list]
            placeholders = ', '.join([f":table{i}" for i in range(len(tables))])
            params = {f'table{i}': table for i, table in enumerate(tables)}
        elif database_type =='MICROSOFTSQLSERVER':
            schema_table_list = [table.split('.') for table in tables_list]
            conditions = ' OR '.join(['(table_schema = ? AND table_name = ?)'] * len(schema_table_list))
            params = [item for sublist in schema_table_list for item in sublist]
        else:
            # Split tables_list into schema and table names
            schema_table_list = [table.split('.') for table in tables_list]
            placeholders = ', '.join([f"(:schema{i}, :table{i})" for i in range(len(schema_table_list))])
            params = {f'schema{i}': schema for i, (schema, table) in enumerate(schema_table_list)}
            params.update({f'table{i}': table for i, (schema, table) in enumerate(schema_table_list)})
        

        if database_type == 'POSTGRESQL':
            query = text(f'''SELECT table_schema, table_name, column_name, data_type
                             FROM information_schema.columns
                             WHERE (table_schema, table_name) IN ({placeholders})''')
        
        elif database_type == 'ORACLE':
            # Adjust schema and table name for Oracle
            params = {f'schema{i}': schema.upper() for i, (schema, table) in enumerate(schema_table_list)}
            params.update({f'table{i}': table.upper() for i, (schema, table) in enumerate(schema_table_list)})
            query = text(f'''SELECT owner AS table_schema, table_name, column_name, data_type
                             FROM all_tab_columns
                             WHERE (owner, table_name) IN ({placeholders})''')
        
        elif database_type == 'MICROSOFTSQLSERVER':
            # query = f'''SELECT table_schema, table_name, column_name, data_type
            #                  FROM INFORMATION_SCHEMA.COLUMNS
            #                  WHERE (table_schema, table_name) IN ({placeholders})'''
            query = f'''SELECT table_schema, table_name, column_name, data_type
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE {conditions}'''
        elif database_type == 'MYSQL':
            query = text(f'''SELECT table_schema, table_name, column_name, data_type
                             FROM information_schema.columns
                             WHERE (table_schema, table_name) IN ({placeholders})''')
        
        elif database_type == 'SQLITE':
            query = text(f'''SELECT name AS table_name, sql
                             FROM sqlite_master
                             WHERE type='table' AND name IN ({placeholders})''')
            with engine.connect() as connection:
                result = connection.execute(query, params)
                tables_info = result.fetchall()
                meta_data = []
                for table in tables_info:
                    table_name, create_sql = table
                    column_definitions = re.search(r'\((.*)\)', create_sql, re.DOTALL).group(1)
                    columns_info = [col.strip() for col in column_definitions.split(',')]
                    for col in columns_info:
                        col_parts = col.split()
                        column_name = col_parts[0].strip('"')
                        data_type = col_parts[1]
                        meta_data.append({"table_name": table_name, "column_name": column_name, "data_type": data_type})
                return {"data": meta_data}
        else:
            return "Unsupported Database Type"

        if database_type == 'MICROSOFTSQLSERVER':
            # Use pyodbc with dynamically constructed query
            query_str = query
            cursor.execute(query_str, params)
            rows = cursor.fetchall()
            meta_data = [{"table_schema": row[0], "table_name": row[1], "column_name": row[2], "data_type": row[3]} for row in rows]
            return {"data": meta_data}
            
        with engine.connect() as connection:
            result = connection.execute(query, params)
            rows = result.fetchall()
            meta_data = [{"table_schema": row[0], "table_name": row[1], "column_name": row[2], "data_type": row[3]} for row in rows]
            return {"data": meta_data}

    except Exception as e:
        return str(e)


format_response = """{
    # use this keys INTEGER, VARCHAR, BOOLEAN, TIMESTAMPTZ for "datatype"
    # INTEGER=['numeric','int','float','number','double precision','smallint','integer','bigint','decimal','numeric','real','smallserial','serial','bigserial','binary_float','binary_double']
    # VARCHAR=['varchar','bp char','text','varchar2','NVchar2','long','char','Nchar','character varying']
    # BOOLEAN=['bool','boolean']
    # TIMESTAMPTZ=['date','time','datetime','timestamp','timestamp with time zone','timestamp without time zone','timezone','time zone'] 
    # Create a Json Body with Specific requiremnt Mentioned accordingly and check String Values in Columns and Numbers in Rows, Check Datatypes mentioned above and Dont Mention existing same column_name in single charts rows and columns
  "charts": [
    {
      "chart_type": "Chart Type",
      "chart_title": "Chart Description",
        # Dont Repeat same column name used in row and col list
      "row": [
        # Row Should Accept Only INTEGER Datatype Columns in row list of Table Meta data
        # Get Row data List should contain, index 0 with column_name, pass "aggregate" in index 1 and index 2 with any of this sum or avg or count or min or max
        [column_name,"aggregate",sum/avg/count/min/max],[column_name,"aggregate",sum/avg/count/min/max]
      ],
      # Col should Accept Only VARCHAR, BOOLEANS AND TIMESTAMPTZ Datatype Columns in col list of table meta data 
      "col": [ 
        [column_name,column datatype,""],[column_name,column datatype,""]
      ]
    }
  ]
}"""    

def can_build_chart(meta_data, prompt):
    if prompt is None:
        return "YES"
    else:
        message = [{'role': 'user', 'content': f"Check whether we can build a chart based on {prompt} and {meta_data}. If we can build, respond with YES; if not, NO"}]
        try:
            API_KEY = get_api_key_from_file()
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                },
                json={
                    "model": "gpt-3.5-turbo-0125",
                    "messages": message,
                    "temperature": 0.7
                }
            )
            # response.raise_for_status()
            response_json = response.json()
            return response_json['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            return {"error": "Error checking chart feasibility. Please try again later."}

def get_gpt_chart_suggestions(meta_data, prompt):
    if prompt is None:
        message = [{'role': 'user', 'content': f"Suggest me some charts based on the meta data provided {meta_data} in this format {format_response} only"}]
    else:
        message = [{'role': 'user', 'content': f"Build {prompt} on the meta data provided {meta_data} in this format {format_response}"}]
    
    try:
        API_KEY = get_api_key_from_file()
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            },
            json={
                "model": "gpt-3.5-turbo-0125",
                "messages": message,
                "temperature": 0.7
            }
        )
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.RequestException as e:
        return {"error": "Error generating chart suggestions. Please try again later."}

def map_columns_to_datatypes(meta_data):
    column_type_map = {}
    for entry in meta_data:
        column_name = entry['column_name']
        data_type = entry['data_type']
        column_type_map[column_name] = data_type
    return column_type_map


def validate_chart_data(data, column_type_map):
    integer_datatypes = ['numeric', 'int', 'float', 'number', 'double precision', 'smallint', 'integer', 'bigint', 'decimal', 'real', 'smallserial', 'serial', 'bigserial', 'binary_float', 'binary_double']
    varchar_datatypes = ['varchar', 'bp char', 'text', 'varchar2', 'NVchar2', 'long', 'char', 'Nchar', 'character varying']
    boolean_datatypes = ['bool', 'boolean']
    timestamptz_datatypes = ['date', 'time', 'datetime', 'timestamp', 'timestamp with time zone', 'timestamp without time zone', 'timezone', 'time zone']

    valid_col_datatypes = varchar_datatypes + boolean_datatypes + timestamptz_datatypes

    corrected_charts = []

    for chart in data['charts']:
        corrected_chart = chart.copy()
        
        # Correct rows: should contain only integer types
        corrected_rows = [
            row for row in chart['row'] if column_type_map.get(row[0]) in integer_datatypes
        ]
        
        # Correct columns: should contain only valid column types
        corrected_cols = [
            col for col in chart['col'] if column_type_map.get(col[0]) in valid_col_datatypes
        ]

        corrected_chart['row'] = corrected_rows
        corrected_chart['col'] = corrected_cols

        corrected_charts.append(corrected_chart)

    return corrected_charts