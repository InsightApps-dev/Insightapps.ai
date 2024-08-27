import os,requests,pdfplumber,boto3,ast,random,re,secrets,string
from project import settings
import pandas as pd
from dashboard import views,models as dshb_models,Connections
from quickbooks import models,serializers
import datetime
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
import json,io


created_at=datetime.datetime.now(utc)
updated_at=datetime.datetime.now(utc)
expired_at=datetime.datetime.now(utc)+datetime.timedelta(minutes=60)


def quickbooks_file_save(qb_id,data1,us_id,disp_name):
    if dshb_models.FileDetails.objects.filter(quickbooks_user_id=qb_id,display_name=disp_name).exists():
        qbmod=dshb_models.FileDetails.objects.get(quickbooks_user_id=qb_id,display_name=disp_name)
        pattern = r'/insightapps/(.*)'
        match = re.search(pattern, qbmod.source)
        dl_key = match.group(1)
    else:
        dl_key=""

    ip='quickbooks'
    fl_tp=dshb_models.FileType.objects.get(file_type="QUICKBOOKS")
    files=Connections.file_save_1(data1,qb_id,us_id,ip,str(dl_key))
    if dshb_models.FileDetails.objects.filter(quickbooks_user_id=qb_id,display_name=disp_name).exists():
        dshb_models.FileDetails.objects.filter(quickbooks_user_id=qb_id,display_name=disp_name).update(source=files['file_url'],updated_at=updated_at)
        qbmod=dshb_models.FileDetails.objects.get(quickbooks_user_id=qb_id,display_name=disp_name)
    else:
        qbmod=dshb_models.FileDetails.objects.create(quickbooks_user_id=qb_id,display_name=disp_name,source=files['file_url'],
                                                uploaded_at=created_at,updated_at=updated_at,user_id=us_id,
                                                file_type=fl_tp.id)
    data = {
        "qb_user_id":qbmod.quickbooks_user_id,
        "file_id":qbmod.id,
        "qb_display_name":qbmod.display_name
    }
    return data
            

def find_key_in_json(data, target_key, results=None):
    if results is None:
        results = []

    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                results.append(value)
            elif isinstance(value, (dict, list)):
                find_key_in_json(value, target_key, results)
    elif isinstance(data, list):
        for item in data:
            find_key_in_json(item, target_key, results)

    return results

def status_check(user_id,qb_id):
    if models.TokenStoring.objects.filter(user=user_id,qbuserid=qb_id).exists():
        data = {
            "status":200,
            "quickbooksConnected":True
        }
    else:
        data = {
            "status":400,
            "message":"please login again in quickbooks",
            "quickbooksConnected":False
        }
    return data


def apis_keys():
    env = settings.ENVIRONMENT
    if env=='sandbox':
        client_id = settings.SANDBOX_QUICKBOOKS_ID
        client_secret = settings.SANDBOX_QUICKBOOKS_SECRET
        redirect_uri = settings.SANDBOX_REDIRECT_URL
        scopes = settings.SANDBOX_SCOPES
        api = settings.SANDBOX_URL
    elif env=='production':
        client_id = settings.PRODUCTION_QUICKBOOKS_ID
        client_secret = settings.PRODUCTION_QUICKBOOKS_SECRET
        redirect_uri = settings.PROPERTY_SANDBOX_REDIRECT_URL
        scopes = settings.PRODUCTION_SCOPES
        api = settings.PRODUCTION_URL
    else:
        return Response({"message":"Not Acceptable"},status=status.HTTP_400_BAD_REQUEST)
    data = {
        "client_id":client_id,
        "client_secret":client_secret,
        "redirect_uri":redirect_uri,
        "scopes":scopes,
        "api":api
    }
    return data



def token_create(redirect_response,user_id,realm_id,display_name):
    try:
        keys = apis_keys()
        oauth = OAuth2Session(keys['client_id'], redirect_uri=keys['redirect_uri'], scope=keys['scopes'])
        token_url = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer'
        token = oauth.fetch_token(token_url, authorization_response=redirect_response, auth=HTTPBasicAuth(keys['client_id'], keys['client_secret']))
        models.TokenStoring.objects.filter(user=user_id,display_name=display_name).delete()
        tb = models.TokenStoring.objects.create(tokentype=token['token_type'],accesstoken=token['access_token'],refreshtoken=token['refresh_token'],display_name=display_name,
                                                idtoken=token['id_token'],updated_at=updated_at,created_at=created_at,expiry_date=expired_at,user=user_id,realm_id=realm_id,
                                                parameter="quickbooks")
        quid = 'QB_'+str(tb.id)+str(tb.user)
        models.TokenStoring.objects.filter(id=tb.id).update(qbuserid=quid)
        data = {
            "status":200,
            "quickbooks_id":tb.qbuserid,
            "message":"Success",
            "quickbooksConnected":True,
            "accesstoken":token['access_token']
        }
        return data
    except:
        data = {
            "status":400,
            "message":"please login again in quickbooks",
            "quickbooksConnected":False,
        }
        return data
        


def acess_refresh_token(refresh_token,user_id,realm_id,qb_id):
    keys = apis_keys()
    token_endpoint = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': keys['client_id'],
        'client_secret': keys['client_secret'],
        'realm_id':realm_id
    }
    response = requests.post(token_endpoint, data=data)
    token_data = response.json()
    if response.status_code == 200:
        # new_access_token = token_data.get('access_token')
        models.TokenStoring.objects.filter(user=user_id,qbuserid=qb_id).update(accesstoken=token_data['access_token'],refreshtoken=token_data['refresh_token'],created_at=created_at,expiry_date=expired_at,realm_id=realm_id)
        data = {
            "status":200,
            "quickbooks_id":qb_id,
            "message":"Success",
            "quickbooksConnected":True,
            "accesstoken":token_data['access_token']
        }
        return data
    else:
        data = {
            "status":400,
            "quickbooksConnected":False,
            "message":token_data,
            "message_status":"please login to quickbboks for token"
        }
        return data


@api_view(['GET'])
def authentication_quickbooks(request,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            keys = apis_keys()
            print(keys['redirect_uri'])
            authorization_base_url = 'https://appcenter.intuit.com/connect/oauth2'
            oauth = OAuth2Session(keys['client_id'], redirect_uri=keys['redirect_uri'], scope=keys['scopes'])
            authorization_url, state= oauth.authorization_url(authorization_base_url)
            data = {
                "redirection_url":authorization_url
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# @api_view(['GET'])
# def qb_callback_api(request):
#     code = request.GET.get('code')
#     if not code:
#         print("Error")
#     keys = apis_keys()
#     parsed_url = urlparse(code)
#     query_params = parse_qs(parsed_url.query)
#     realm_id = query_params.get('realmId', [None])[0]
#     oauth = OAuth2Session(keys['client_id'], redirect_uri=keys['redirect_uri'], scope=keys['scopes'])
#     token_url = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer'
#     token = oauth.fetch_token(token_url, authorization_response=code, auth=HTTPBasicAuth(keys['client_id'], keys['client_secret']))
#     data = {
#         'realm_id':realm_id,
#         'token_type':token['token_type'],
#         'access_token':token['access_token'],
#         'refresh_token':token['refresh_token'],
#         'id_token':token['id_tokn']
#     }
#     print(data)
#     return Response(data,status=status.HTTP_200_OK)


##### GET the token from reirect url
class token_api(CreateAPIView):
    serializer_class = serializers.token_serializer

    def post(self,request,token):
        tok1 = views.test_token(token)
        if tok1['status']==200:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                redirect_response1 = serializer.validated_data['redirect_url']
                display_name = serializer.validated_data['display_name']
                r1 = settings.token_url
                redirect_response = str(r1)+str(redirect_response1)
                parsed_url = urlparse(redirect_response)
                query_params = parse_qs(parsed_url.query)
                realm_id = query_params.get('realmId', [None])[0]
                parameter="quickbooks"
                if models.TokenStoring.objects.filter(user=tok1['user_id'],display_name=display_name,parameter=parameter).exists():
                    return Response({'message':'Display name already exists, please change display name'},status=status.HTTP_406_NOT_ACCEPTABLE)
                ac_token=token_create(redirect_response,tok1['user_id'],realm_id,display_name)
                if ac_token['status']==200:
                    return Response(ac_token,status=status.HTTP_200_OK)
                elif ac_token['status']==400:
                    if models.TokenStoring.objects.filter(user=tok1['user_id'],display_name=display_name,parameter=parameter).exists():
                        tokac = models.TokenStoring.objects.get(user=tok1['user_id'],display_name=display_name,parameter=parameter)
                        if tokac.expiry_date < datetime.datetime.now(utc):#+datetime.timedelta(hours=5,minutes=30)
                            refer = acess_refresh_token(tokac.refreshtoken,tok1['user_id'],realm_id,tokac.qbuserid)
                            if refer['status']==200:
                                return Response(refer,status=status.HTTP_200_OK)
                            else:
                                return Response(refer,status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"message":"Success","quickbooksConnected":True},status=status.HTTP_200_OK)
                else:
                    return Response(ac_token,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"Serializer value error"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(tok1,status=tok1['status'])


##### Disconnection quickbooks 

@api_view(['DELETE'])
def qb_disconnection(request,qb_id,token):
    if request.method=='DELETE':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            tokst=status_check(tok1['user_id'],qb_id)
            if tokst['status']==200:
                models.TokenStoring.objects.filter(user=tok1['user_id'],qbuserid=qb_id).delete()
                dshb_models.FileDetails.objects.filter(quickbooks_user_id=qb_id).delete()
                return Response({"message":"Disconnected from quickbooks","quickbooksConnected":False},status=status.HTTP_200_OK)
            else:
                return Response(tokst,status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

###### GET user details from quickbooks ###
@api_view(['GET'])
def get_quickbooks_user_info(request,qb_id,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            tokst=status_check(tok1['user_id'],qb_id)
            if tokst['status']==200:
                tokac = models.TokenStoring.objects.get(user=tok1['user_id'],qbuserid=qb_id)
                if settings.ENVIRONMENT == 'sandbox':
                    url = 'https://sandbox-accounts.platform.intuit.com/v1/openid_connect/userinfo'
                else:
                    url = 'https://accounts.platform.intuit.com/v1/openid_connect/userinfo'
                headers = {
                    'Authorization': f'Bearer {tokac.accesstoken}',
                    'Accept': 'application/json'
                }
                response = requests.get(url, headers=headers)
                if response.status_code==200:
                    return Response({'message':'success','data':response.json()},status=status.HTTP_200_OK)
                else:
                    return response({'message':response},status=response.status_code)
            else:
                return Response(tokst,status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
