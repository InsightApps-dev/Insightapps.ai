import os,requests,pdfplumber,boto3,ast,random,re,secrets,string
from project import settings
import pandas as pd
import pkce,base64,hashlib
from dashboard import views
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
import urllib.parse
import requests
from django.shortcuts import redirect


created_at=datetime.datetime.now(utc)
updated_at=datetime.datetime.now(utc)
expired_at=datetime.datetime.now(utc)+datetime.timedelta(hours=12)

def apis_keys():
    client_id = settings.SALESFORCE_CONSUMER_KEY
    client_secret = settings.SALESFORCE_CONSUMER_SECRET
    redirect_uri = settings.SALESFORCE_REDIRECT_URI
    auth_url = settings.SALESFORCE_AUTH_URL
    toke_url = settings.SALESFORCE_TOKEN_URL
    data = {
        "client_id":client_id,
        "client_secret":client_secret,
        "redirect_uri":redirect_uri,
        "auth_url":auth_url,
        "tok_url":toke_url
    }
    return data


def token_create(user_id,display_name,token,parameter):
    try:
        models.TokenStoring.objects.filter(user=user_id,display_name=display_name,parameter=parameter).delete()
        tb = models.TokenStoring.objects.create(tokentype=token['token_type'],accesstoken=token['access_token'],refreshtoken=token['refresh_token'],display_name=display_name,
                                                idtoken=token['id_token'],updated_at=updated_at,created_at=created_at,expiry_date=expired_at,user=user_id,
                                                parameter=parameter)
        sfid = 'SF_'+str(tb.id)+str(tb.user)
        models.TokenStoring.objects.filter(id=tb.id).update(salesuserid=sfid)
        data = {
            "status":200,
            "salesforce_id":tb.salesuserid,
            "message":"Success",
            "SalesforceConnected":True,
            "accesstoken":token['access_token']
        }
        return data
    except:
        data = {
            "status":400,
            "message":"please login again in salesforce",
            "SalesforceConnected":False,
        }
        return data


# def callback_api(request):
#     code = request.GET.get('code')
#     if code:
#         # Redirect to a route that will handle the token exchange
#         return redirect(f'/token_fetch/?code={code}')
#     # return HttpResponse("Error: No code found in request.", status=400)


class callback_api(CreateAPIView):
    serializer_class=serializers.display_name

    @transaction.atomic
    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            display_name=serializer.validated_data['display_name']
            token=serializer.validated_data['token']
            tok1 = views.test_token(token)
            if tok1['status']==200:
                keys = apis_keys()
                code = request.GET.get('code')
                print(code)
                if not code:
                    return Response({'message':'Code error'},status=status.HTTP_400_BAD_REQUEST)
                data = {
                    'grant_type': 'authorization_code',
                    'code': code,
                    'client_id': keys['client_id'],
                    'client_secret': keys['client_secret'],
                    'redirect_uri': keys['redirect_uri']
                }
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                response = requests.post(keys['tok_url'], data=data, headers=headers)
                if response.status_code==200:
                    token_data = response.json()
                    token=token_create(tok1['user_id'],display_name,token_data,parameter="salesforce")
                    if token['status']==200:
                        return Response(token,status=status.HTTP_200_OK)
                    else:
                        return Response(token,status=token['status'])
                else:
                    return Response(response,status=response.status_code)
            else:
                return Response(tok1,status=tok1['status'])
        else:
            return Response({'message':'serializer value error'},status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def authentication_salesforce(request,token):
    if request.method=='POST':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            keys = apis_keys()
            params = {
                'response_type': 'code',
                'client_id': keys['client_id'],
                'redirect_uri': keys['redirect_uri'],
                # 'scope':'full'
                'scope': 'offline_access full'
            }
            login_url = f"{keys['auth_url']}?{urllib.parse.urlencode(params)}"
            return Response(login_url,status=status.HTTP_200_OK)
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def refresh_access_token(request,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            keys = apis_keys()
            refresh_token='5Aep861njAMw_1t53tLB1pa.bbkcHkozXvD1q3IISLFva5Ig7Z0DpoMkTo0yPCQsEe7wLd_hOHbe6QqtpRkfTKw'
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': keys['client_id'],
                'client_secret': keys['client_secret']
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.post(keys['tok_url'], data=data, headers=headers)
            print(response.status_code)
            if response.status_code == 200:
                try:
                    token_data = response.json()
                    return Response(token_data,status=status.HTTP_200_OK)
                except ValueError:
                    return "Error: Invalid response format."
            else:
                return Response(response,status=response.status_code)
        else:
            return Response(tok1,status=tok1['status'])
    else:
        return Response({"message":"Method not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)




@api_view(['GET'])
def get_salesforce_user_info(request,token):
    if request.method=='GET':
        tok1 = views.test_token(token)
        if tok1['status']==200:
            domain = 'https://stratapps6-dev-ed.develop.my.salesforce.com'
            url = f"{domain}/services/oauth2/userinfo"
            access_token= '00DdL000008yL4z!AQEAQEF73Adm6pa_2by7ztvj_Abk8AMdk5EWzzm7QxLiLazegSE2lMEMbou8BsWq63LVAaWD_I93YE36J04wO94W6OuMTRGa'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(url, headers=headers)
            print(response.status_code)
            print(response)
            print(response.json())
            # return response.json()