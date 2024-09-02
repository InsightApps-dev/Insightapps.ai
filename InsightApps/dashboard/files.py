import os,requests,pdfplumber,boto3
from project import settings
import pandas as pd
from dashboard import views,serializers,models,roles,previlages,Connections
import datetime,re
from io import BytesIO
from pytz import utc
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from pathlib import Path
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile



def get_file_extension(uploaded_file):
    file_name, file_extension = os.path.splitext(uploaded_file.name)
    return file_extension

def get_file_name(uploaded_file):
    file_name, file_extension = os.path.splitext(uploaded_file.name)
    return file_name


def read_excel_file(file_path,filename,file_id):
    try:
        xls = pd.ExcelFile(file_path)
        result = {"schemas": []}
        l=[]
        file_n=Path(str(file_path))
        cleaned_name = re.sub(r'^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', '', str(filename))
        for i in xls.sheet_names:
            data_csv = pd.read_excel(file_path,sheet_name=i)
            data_csv = data_csv.fillna(value='NA')
            headers = data_csv.columns.tolist()

            l.append({"schema":cleaned_name,"table":i,"columns":[{'column':colm,'datatypes':None} for colm in headers]})
            # data ={
            #     # "schemas":filename,
            #     "schemas":a,
            #     # "table":i,
            #     # "sheet_name":i,
            #     # "data":data_csv,  ## file data
            #     # "columns":[{'columns':colm,'datatypes':None} for colm in headers]
            # }
            # l.append(data)
        result["schemas"].append({"schema": cleaned_name, "tables": l})

        f_dt={
            "status":200,
            "message":"Successfully Connected to file",
            "data":result,
            "file_id":file_id,
            "filename":cleaned_name,
            "display_name":cleaned_name
        }
        return f_dt
    except Exception as e:
        f_dt = {
            "status":400,
            "message":e
        }
        return f_dt



def read_csv_file(file_path,filename,file_id):
    try:
        df = pd.read_csv(file_path)
        df = df.fillna(value='NA')
        headers = df.columns.tolist()
        file_n=Path(str(file_path))
        result = {"schemas": []}
        l1=[]
        # d1 = {
        #     "schema":filename,
        #     "table":filename,
        #     "sheet_name":filename,
        #     "columns":[{'columns':colm,'datatypes':None} for colm in headers]
        # }
        # l1.append(d1)
        cleaned_name = re.sub(r'^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', '', str(file_n.stem))
        l1.append({"schema":cleaned_name,"table":cleaned_name,"columns":[{'column':colm,'datatypes':None} for colm in headers]})
        result["schemas"].append({"schema": filename, "tables": l1})
        f_dt={
            "status":200,
            "message":"Successfully Connected to file",
            "file_id":file_id,
            "filename":filename,
            "sheet_names":[cleaned_name],
            # "data":df
            "data":result,
            "display_name":filename
        }
        return f_dt
    except Exception as e:
        f_dt = {
            "status":400,
            "message":e
        }
        return f_dt


def read_pdf_file(file_path,filename,file_id):
    try:
        appended_data1 = pd.DataFrame()
        response2 = requests.get(file_path)
        pdf_data1 = BytesIO(response2.content)
        with pdfplumber.open(pdf_data1) as pdf1:
            for pageno in range(len(pdf1.pages)):
                page = pdf1.pages[pageno]
                data = page.extract_table()
                # data = page.extract_text_lines()
                df=pd.DataFrame(data)
                for index, row in df.iterrows():
                    row_df = pd.DataFrame([row])
                    appended_data1 = pd.concat([appended_data1, row_df], ignore_index=True)
        f_dt={
            "status":200,
            "message":"Successfully Connected to file",
            "file_id":file_id,
            "filename":filename,
            "sheet_names":filename,
            # "dataframe":df,
            "data":list(appended_data1)
        }
        return f_dt
    except Exception as e:
        f_dt = {
            "status":400,
            "message":e
        }
        return f_dt

def read_text_file(file_path,filename,file_id):
    try:
        response = requests.get(file_path)
        data = response.text
        data_list = data.split()
        l=[]
        for line in data_list:
            l.append(line)
        f_dt={
            "status":200,
            "message":"Successfully Connected to file",
            "file_id":file_id,
            "filename":filename,
            "sheet_names":filename,
            # "dataframe":df,
            "data":l
        }
        return f_dt
    except Exception as e:
        f_dt = {
            "status":400,
            "message":e
        }
        return f_dt
    
# def read_xml_file(file_path):
#     try:
#         df = pd.read_xml(file_path)
#         return df
#     except Exception as e:
#         return Response(f'{e}',status=status.HTTP_400_BAD_REQUEST)
    
class UploadFileAPI(CreateAPIView):
    serializer_class = serializers.UploadFileSerializer
    
    @transaction.atomic()
    def post(self, request,token):
        role_list=roles.get_previlage_id(previlage=[previlages.create_csv_files,previlages.view_csv_files,previlages.create_excel_files,previlages.view_excel_files])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                file_type = serializer.validated_data['file_type']
                file_path112 = serializer.validated_data['file_path']
                s3 = boto3.client('s3', aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY)
                filename = get_file_name(file_path112)
                fileext = get_file_extension(file_path112)
                file_path=file_path112.name.replace('_','').replace(' ','').replace('&','') ## to clean the unnecessary spaces in file name

                file_save=Connections.file_files_save(file_path,file_path112)
                file_url=file_save['file_url']
                file_path1=file_save['file_key']

                if models.FileType.objects.filter(file_type=file_type.upper()).exists:
                    ft = models.FileType.objects.get(file_type=file_type.upper())
                    file_cr=models.FileDetails.objects.create(
                        file_type = ft.id,
                        source = file_url,
                        datapath=file_path1,
                        display_name = str(file_path),
                        user_id = tok1['user_id'],
                    )
                    if file_type.upper()=='EXCEL' and fileext == '.xlsx' or file_type.upper()=='EXCEL' and fileext == '.xls':
                        data = read_excel_file(file_url,filename,file_cr.id)
                    elif  file_type.upper()=='CSV' and fileext == '.csv':
                        data = read_csv_file(file_url,filename,file_cr.id)
                    elif file_type.upper()=='PDF' and fileext == '.pdf':
                        data = read_pdf_file(file_url,filename,file_cr.id)
                    elif file_type.upper()=='TEXT' and fileext == '.txt':
                        data = read_text_file(file_url,filename,file_cr.id)
                    # elif fileext == '.xml':
                    #     data = read_xml_file(file_url)
                    #     data = json.dumps(data)
                    else:
                        return Response({'error': 'Unsupported file type/format'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    if data['status']==200:
                        return Response(data,status=status.HTTP_200_OK)
                    else:
                        return Response(data,status=data['status'])
                else:
                    return Response({'error': 'Unsupported file type'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:  
                return Response("Serializer Error", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(tok1,status=tok1['status'])
        

@api_view(['GET'])
def files_data_fetch(request,file_id,token):
    if request.method=='GET':
        role_list=roles.get_previlage_id(previlage=[previlages.view_excel_files,previlages.view_csv_files])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            if models.FileDetails.objects.filter(id=file_id,user_id=tok1['user_id']).exists():
                file=models.FileDetails.objects.get(id=file_id,user_id=tok1['user_id'])
                fi_type=models.FileType.objects.get(id=file.file_type)
                filename = re.sub(r'^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', '', file.display_name)
                if fi_type.file_type=='EXCEL':
                    data = read_excel_file(file.source,filename,file.id)
                elif fi_type.file_type=='CSV':
                    data = read_csv_file(file.source,filename,file.id)
                elif fi_type.file_type=='PDF':
                    data = read_pdf_file(file.source,filename,file.id)
                elif fi_type.file_type=='TEXT':
                    data = read_text_file(file.source,filename,file.id)
                else:
                    return Response({'error': 'Unsupported file type/format'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                if data['status']==200:
                    return Response(data,status=status.HTTP_200_OK)
                else:
                    return Response(data,status=data['status'])
            else:
                return Response({'message':'File not found'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({'message':'Method Not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['DELETE'])
def files_delete(request,file_id,token):
    if request.method=='DELETE':
        role_list=roles.get_previlage_id(previlage=[previlages.delete_csv_files,previlages.delete_excel_files])
        tok1 = roles.role_status(token,role_list)
        if tok1['status']==200:
            if models.FileDetails.objects.filter(id=file_id,user_id=tok1['user_id']).exists():
                file=models.FileDetails.objects.get(id=file_id,user_id=tok1['user_id'])
                # pattern = r'/insightapps/(.*)'
                # match = re.search(pattern, file.source)
                # result = match.group(1)
                # s3 = boto3.client('s3', aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY)
                # s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=str(result))
                qr_list=models.QuerySets.objects.filter(file_id=file.id).values()
                for qr_id in qr_list:
                    sh_dt=models.sheet_data.objects.filter(queryset_id=qr_id['queryset_id']).values()
                    for qr in sh_dt:
                        dsdt=models.dashboard_data.objects.filter(sheet_ids__contains=str(qr['id'])).values()
                        Connections.sheet_ds_delete(dsdt,qr['id'],file.id,qr_id['queryset_id'])
                    models.QuerySets.objects.filter(queryset_id=qr_id['queryset_id']).delete()
                    models.DataSource_querysets.objects.filter(queryset_id=qr_id['queryset_id']).delete()
                    models.DataSourceFilter.objects.filter(queryset_id=qr_id['queryset_id']).delete()
                    models.sheet_data.objects.filter(queryset_id=qr_id['queryset_id']).delete()
                    models.SheetFilter_querysets.objects.filter(queryset_id=qr_id['queryset_id']).delete()
                    models.ChartFilters.objects.filter(queryset_id=qr_id['queryset_id']).delete()
                    models.DashboardFilters.objects.filter(queryset_id=qr_id['queryset_id']).delete()
                models.FileDetails.objects.filter(id=file_id,user_id=tok1['user_id']).delete()
                Connections.delete_file(file.datapath)
                return Response({'message':'File deleted successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'message':'File not found'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({'message':'Method Not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)