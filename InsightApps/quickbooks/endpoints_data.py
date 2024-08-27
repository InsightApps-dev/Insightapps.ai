import os,requests,pdfplumber,boto3,ast,random,re,secrets,string
from project import settings
import pandas as pd
from dashboard import views,models as dshb_models
from quickbooks import models,serializers as qb_seria,views as qb_views
import datetime
from datetime import timedelta
from io import BytesIO
from pytz import utc
from requests.auth import HTTPBasicAuth
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.template.loader import render_to_string
from django.core.mail import send_mail
from urllib.parse import urlparse, parse_qs
from requests_oauthlib import OAuth2Session


created_at=datetime.datetime.now(utc)
updated_at=datetime.datetime.now(utc)


def query_details(user_id,query,qb_id,display_name):
    tokst=qb_views.status_check(user_id,qb_id)
    if tokst['status']==200:
        tokac=models.TokenStoring.objects.get(user=user_id,qbuserid=qb_id)
        if tokac.expiry_date > datetime.datetime.now(utc):
            pass
        else:
            rftk=qb_views.acess_refresh_token(tokac.refreshtoken,user_id,tokac.realm_id,qb_id)
            if rftk['status']==200:
                tokac = models.TokenStoring.objects.get(user=user_id,qbuserid=qb_id)
            else:
                return Response(rftk,status=status.HTTP_400_BAD_REQUEST)
        keys = qb_views.apis_keys()
        query = 'select * from '+str(query)
        api_url = "{}/v3/company/{}/query?query={}&minorversion=69".format(keys['api'],int(tokac.realm_id),query)
        headers = {
            'Authorization': f'Bearer {tokac.accesstoken}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = requests.request("GET", api_url, headers=headers)
        data = response.json()
        if response.status_code == 200:
            data1 = {
                "propertyquickbooksConnected":True,
                "status":data
            }
            qb_file=qb_views.quickbooks_file_save(qb_id,data1,user_id,disp_name=display_name)
            data1["qb_file_data"]=qb_file
            return Response(data1, status=status.HTTP_200_OK)
        else:
            data1 = {
                "propertyquickbooksConnected":False,
                "status":data
            }
            return Response(data1,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(tokst,status=status.HTTP_401_UNAUTHORIZED)



##### Fetching BalanceSheet
class fetch_Balancesheet_details(CreateAPIView):
    serializer_class = qb_seria.filter_date

    def post(self,request,qb_id,token):
        tok1 = views.test_token(token)
        if tok1['status']==200:
            tokst=qb_views.status_check(tok1['user_id'],qb_id)
            if tokst['status']==200:
                tokac=models.TokenStoring.objects.get(user=tok1['user_id'],qbuserid=qb_id)
                if tokac.expiry_date > datetime.datetime.now(utc):
                    pass
                else:
                    rftk=qb_views.acess_refresh_token(tokac.refreshtoken,tok1['user_id'],tokac.realm_id,qb_id)
                    if rftk['status']==200:
                        tokac = models.TokenStoring.objects.get(user=tok1['user_id'],qbuserid=qb_id)
                    else:
                        return Response(rftk,status=status.HTTP_400_BAD_REQUEST)
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    from_date = serializer.validated_data['from_date']
                    to_date = serializer.validated_data['to_date']
                    if from_date!='' and to_date!='':
                        if from_date < to_date:
                            pass
                        else:
                            return Response({"message":"Start Date Must Be Less Than End Date"},status=status.HTTP_406_NOT_ACCEPTABLE)
                    else:
                        pass
                    keys = qb_views.apis_keys()
                    api_url = "{}/v3/company/{}/reports/BalanceSheet?end_date={}&start_date={}&minorversion=69".format(keys['api'],int(tokac.realm_id),to_date,from_date)
                    account_data = {
                        "end_date":str(to_date),
                        "start_date":str(from_date)
                    }
                    headers = {
                        'Authorization': f'Bearer {tokac.accesstoken}',
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    }
                    response = requests.request("GET", api_url, json=account_data, headers=headers)
                    data = response.json()
                    desired_key = 'ColData'
                    results = qb_views.find_key_in_json(data, desired_key)
                    if response.status_code == 200:
                        data1 = {
                            "propertyquickbooksConnected":True,
                            "Header":data['Header'],
                            "Columns":data['Columns'],
                            "results":results
                        }
                        qb_file=qb_views.quickbooks_file_save(qb_id,data1,tok1['user_id'],disp_name="balance_sheet")
                        data1["qb_file_data"]=qb_file
                        return Response(data1, status=status.HTTP_200_OK)
                    else:
                        data1 = {
                            "propertyquickbooksConnected":False,
                            "status":data
                        }
                        return Response(data1,status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":"Serializer value error"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(tokst,status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(tok1,status=tok1['status'])



##### Fetching profitloss
class fetch_profitloss_details(CreateAPIView):
    serializer_class = qb_seria.filter_date

    def post(self,request,qb_id,token):
        tok1 = views.test_token(token)
        if tok1['status']==200:
            tokst=qb_views.status_check(tok1['user_id'],qb_id)
            if tokst['status']==200:
                tokac=models.TokenStoring.objects.get(user=tok1['user_id'],qbuserid=qb_id)
                if tokac.expiry_date > datetime.datetime.now(utc)+timedelta(hours=5,minutes=30):
                    pass
                else:
                    rftk=qb_views.acess_refresh_token(tokac.refreshtoken,tok1['user_id'],tokac.realm_id,qb_id)
                    if rftk['status']==200:
                        tokac = models.TokenStoring.objects.get(user=tok1['user_id'],qbuserid=qb_id)
                    else:
                        return Response(rftk,status=status.HTTP_400_BAD_REQUEST)
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    from_date = serializer.validated_data['from_date']
                    to_date = serializer.validated_data['to_date']
                    if from_date!='' and to_date!='':
                        if from_date < to_date:
                            pass
                        else:
                            return Response({"message":"Start Date Must Be Less Than End Date"},status=status.HTTP_406_NOT_ACCEPTABLE)
                    else:
                        pass
                    keys = qb_views.apis_keys()
                    api_url = "{}/v3/company/{}/reports/ProfitAndLoss?start_date={}&end_date={}&minorversion=69".format(keys['api'],int(tokac.realm_id),from_date,to_date)
                    # start_date must be less than end_date #YYYY-MM-DD format only.
                    account_data = {
                        "end_date":str(to_date),
                        "start_date":str(from_date)
                    }
                    headers = {
                        'Authorization': f'Bearer {tokac.accesstoken}',
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    }
                    response = requests.request("GET", api_url, json=account_data, headers=headers)
                    data = response.json()
                    desired_key = 'ColData'
                    results = qb_views.find_key_in_json(data, desired_key)
                    if response.status_code == 200:
                        data1 = {
                            "propertyquickbooksConnected":True,
                            "Header":data['Header'],
                            "Columns":data['Columns'],
                            "results":results
                        }
                        qb_file=qb_views.quickbooks_file_save(qb_id,data1,tok1['user_id'],disp_name="profit_and_loss")
                        data1["qb_file_data"]=qb_file
                        return Response(data1, status=status.HTTP_200_OK)
                    else:
                        data1 = {
                            "propertyquickbooksConnected":False,
                            "status":data
                        }
                        return Response(data1,status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":"Serializer value error"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(tokst,status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(tok1,status=tok1['status'])
        

        
##### Fetching Accounts
@api_view(['GET'])
def fetch_quickbooks_account(request,qb_id,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            query='Account order by Id desc'
            qr=query_details(tok1['user_id'],query,qb_id,display_name="account_details")
            return qr
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)


##### Fetching Bills
@api_view(['GET'])
def fetch_Bill_details(request,qb_id,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            query='bill order by Id desc'
            qr=query_details(tok1['user_id'],query,qb_id,display_name="bill_details")
            return qr
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        

##### Fetching company details
@api_view(['GET'])
def fetch_company_details(request,qb_id,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            query='CompanyInfo'
            qr=query_details(tok1['user_id'],query,qb_id,display_name="company_details")
            return qr
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


##### Fetching Customer Details
@api_view(['GET'])
def fetch_customer_details(request,qb_id,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            query='Customer order by Id desc'
            qr=query_details(tok1['user_id'],query,qb_id,display_name="customer_details")
            return qr
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)



##### Fetching Employee Details
@api_view(['GET'])
def fetch_employee_details(request,qb_id,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            query='Employee order by Id desc'
            qr=query_details(tok1['user_id'],query,qb_id,display_name="employee_details")
            return qr
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        


##### Fetching Estimate Details
@api_view(['GET'])
def fetch_estimate_details(request,qb_id,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            query='estimate order by Id desc'
            qr=query_details(tok1['user_id'],query,qb_id)
            return qr
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


##### Fetching Invoice Details
@api_view(['GET'])
def fetch_invoice_details(request,qb_id,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            query='Invoice order by Id desc'
            qr=query_details(tok1['user_id'],query,qb_id,display_name="invoice_details")
            return qr
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


##### Fetching Item Details
@api_view(['GET'])
def fetch_item_details(request,qb_id,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            query='Item order by Id desc'
            qr=query_details(tok1['user_id'],query,qb_id,display_name="items_details")
            return qr
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


##### Fetching Payment Details
@api_view(['GET'])
def fetch_payment_details(request,qb_id,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            query='Payment order by Id desc'
            qr=query_details(tok1['user_id'],query,qb_id,display_name="payment_details")
            return qr
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


##### Fetching Preferences Details
@api_view(['GET'])
def fetch_Preferences_details(request,qb_id,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            query='Preferences'
            qr=query_details(tok1['user_id'],query,qb_id)
            return qr
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


##### Fetching TaxAgency Details
@api_view(['GET'])
def fetch_TaxAgency_details(request,qb_id,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            query='TaxAgency order by Id desc'
            qr=query_details(tok1['user_id'],query,qb_id,display_name="tax_agency_details")
            return qr
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

##### Fetching Vendors
@api_view(['GET'])
def fetch_vendor_details(request,qb_id,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            query='vendor order by Id desc'
            qr=query_details(tok1['user_id'],query,qb_id,display_name="vendor_details")
            return qr
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
