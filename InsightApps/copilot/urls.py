from django.urls import path
from .views import *

urlpatterns = [
    path('copilot/',GetServerTablesList.as_view(),name='Get Query Set Details'),
    path('validate-api-key/', ValidateApiKeyView.as_view(), name='validate-api-key'),
]