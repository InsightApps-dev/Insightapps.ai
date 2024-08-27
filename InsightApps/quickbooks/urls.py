from django.urls import path
from quickbooks import views,endpoints_data,salesforce

urlpatterns = [
    #### sales force
    path('salesforce/<token>',salesforce.authentication_salesforce,name='sales force authentication'),
    path('callback/',salesforce.callback_api.as_view(),name='call back'),
    path('sales_user_details/<token>',salesforce.get_salesforce_user_info,name='user details'),
    path('refresh_token/<token>',salesforce.refresh_access_token,name='user details'),

    #### authentication
    path('quickbooks/<token>',views.authentication_quickbooks,name='quickbooks authentication'),
    path('quickbooks_token/<token>',views.token_api.as_view(),name='token fetch'),
    path('user_details/<qb_id>/<token>',views.get_quickbooks_user_info,name='user details'),
    path('quickbooks_disconnection/<qb_id>/<token>',views.qb_disconnection,name='quickbooks disconnection'),

    ##### Endpoints data
    path('balance_sheet/<qb_id>/<token>',endpoints_data.fetch_Balancesheet_details.as_view(),name='Balance sheet'),
    path('profitandloss/<qb_id>/<token>',endpoints_data.fetch_profitloss_details.as_view(),name='profit and loss'),
    path('accountsdetails/<qb_id>/<token>',endpoints_data.fetch_quickbooks_account,name='account details'),
    path('billdetails/<qb_id>/<token>',endpoints_data.fetch_Bill_details,name='bill details'),
    path('companydetails/<qb_id>/<token>',endpoints_data.fetch_company_details,name='company details'),
    path('customerdetails/<qb_id>/<token>',endpoints_data.fetch_customer_details,name='customer details'),
    path('employeedetails/<qb_id>/<token>',endpoints_data.fetch_employee_details,name='employee details'),
    path('invoicedetails/<qb_id>/<token>',endpoints_data.fetch_invoice_details,name='invoice details'),
    path('itemdetails/<qb_id>/<token>',endpoints_data.fetch_item_details,name='item details'),
    path('paymentdetails/<qb_id>/<token>',endpoints_data.fetch_payment_details,name='payment details'),
    path('taxagencydetails/<qb_id>/<token>',endpoints_data.fetch_TaxAgency_details,name='tax agency details'),
    path('vendordetails/<qb_id>/<token>',endpoints_data.fetch_vendor_details,name='vendor details'),
]
