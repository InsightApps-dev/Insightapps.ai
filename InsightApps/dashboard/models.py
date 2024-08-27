from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserProfile(AbstractUser):
    id = models.AutoField(primary_key=True,db_column='user_id')
    name = models.CharField(max_length=100,null=True)
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(db_column='email_id',unique=True)
    password = models.CharField(max_length=256)
    is_active = models.BooleanField(db_column='is_active',default=False)
    sub_identifier = models.CharField(max_length=100,null=True,unique=True)
    country = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    class Meta:
        db_table="user_profile"
        
custom_expiry_date = datetime.datetime.now()+datetime.timedelta(days=2)
class Account_Activation(models.Model):
    user = models.IntegerField(db_column='user_id', null=True)
    email = models.CharField(max_length=50, null=True,blank=True,default='')
    key = models.CharField(max_length=100, blank=True, null=True)
    otp = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    expiry_date = models.DateTimeField(default=custom_expiry_date)

    class Meta:
        db_table = 'account_activation'
        
class Reset_Password(models.Model):
    user = models.IntegerField(db_column='user_id', null=True)
    key = models.CharField(max_length=32, blank=True, null=False, db_column='key')
    created_at = models.DateTimeField(default=datetime.datetime.now())
    class Meta:
        db_table = 'reset_password'

class Role(models.Model):
    role_id =models.AutoField(primary_key=True)
    created_by = models.IntegerField(null=True,blank=True)
    role = models.CharField(max_length=40,blank=True, null=True)
    previlage_id = models.CharField(max_length=1000,db_column='previlage_id',null=True,blank=True)
    role_desc = models.CharField(max_length=255, null=True,default='role_description')
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        db_table = 'role'


class previlages(models.Model):
    id = models.AutoField(primary_key=True)
    previlage = models.CharField(max_length=2000,null=True,blank=True)

    class Meta:
        db_table= 'previlages'

class UserRole(models.Model):
    id = models.AutoField(primary_key=True,db_column='id')
    role_id = models.IntegerField( db_column='role_id')
    user_id = models.IntegerField(db_column='user_id')

    class Meta:
        db_table= 'user_role'
        unique_together = (('role_id', 'user_id'))


class FileType(models.Model):
    id = models.AutoField(primary_key=True,db_column='file_type_id')
    file_type = models.CharField(max_length=50,db_column='file_type',unique=True)
    
    class Meta:
        db_table = 'file_type'
    
class FileDetails(models.Model):
    id  = models.AutoField(primary_key=True,db_column='file_details_id')
    file_type = models.PositiveBigIntegerField(db_column='file_type_id')
    source = models.CharField(max_length=500,null=True,blank=True,db_column='source_path')
    display_name = models.CharField(max_length=500,null=True,db_column='display_name')
    uploaded_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.PositiveBigIntegerField(db_column='user_id')
    quickbooks_user_id = models.CharField(max_length=100,null=True,blank=True)
    
    class Meta:
        db_table = 'file_details'

class ServerType(models.Model):
    id = models.AutoField(primary_key=True,db_column='server_type_id')
    server_type = models.CharField(max_length=50,db_column='server_type',unique=True)
    
    class Meta:
        db_table = 'server_type'
        

class ServerDetails(models.Model):
    id  = models.AutoField(primary_key=True,db_column='server_details_id')
    server_type = models.PositiveBigIntegerField(db_column='server_type_id')
    hostname = models.CharField(max_length=500,null=True,db_column='hostname')
    username = models.CharField(max_length=500,null=True,db_column='username')
    password = models.CharField(max_length=500,null=True,db_column='password')
    database = models.CharField(max_length=500,null=True,db_column='database')
    database_path = models.CharField(max_length=1500,null=True,db_column='database_path')
    service_name = models.CharField(max_length=500,null=True,db_column='service_name')
    port = models.IntegerField(null=True,db_column='port')
    display_name = models.CharField(max_length=500,null=True,db_column='display_name')
    is_connected = models.BooleanField(default=True)
    user_id = models.IntegerField(null=True,db_column='user_id')
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'server_details'
        
class QuerySets(models.Model):
    queryset_id  = models.AutoField(primary_key=True, db_column='queryset_id')
    user_id = models.IntegerField(db_column='user_id')
    server_id = models.IntegerField(null=True,blank=True)
    file_id = models.CharField(max_length=100,null=True,blank=True)
    table_names = models.TextField()
    join_type = models.TextField()
    joining_conditions = models.TextField()
    is_custom_sql = models.BooleanField(default=False)
    custom_query = models.TextField()
    query_name = models.CharField(null=True,blank=True,max_length=500,db_column = 'query_name')
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)
    datasource_path = models.CharField(max_length=200,null=True,db_column='datasource_filename')
    datasource_json =models.URLField(null=True,db_column = 'datasource_json_url')
    class Meta:
        db_table = 'querysets'

class DataSource_querysets(models.Model):
    datasource_querysetid = models.AutoField(primary_key=True)
    queryset_id  = models.IntegerField()
    user_id = models.IntegerField(db_column='user_id')
    server_id = models.IntegerField(null=True,blank=True)
    file_id = models.IntegerField(null=True,blank=True)
    table_names = models.TextField()
    filter_id_list = models.TextField()
    is_custom_sql = models.BooleanField(default=False)
    custom_query = models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'datasource_querysets'
        
class ChartFilters(models.Model):
    filter_id = models.AutoField(primary_key=True,db_column='filter_id')
    user_id = models.IntegerField(db_column='user_id')
    server_id = models.IntegerField(null=True,blank=True)
    file_id = models.IntegerField(null=True,blank=True)
    datasource_querysetid = models.IntegerField(null=True,blank=True)
    queryset_id  = models.IntegerField(null=True,blank=True)
    col_name = models.CharField(max_length = 500)
    data_type = models.CharField(max_length = 500)
    filter_data = models.TextField(null=True)
    row_data = models.TextField(null=True)
    format_type = models.CharField(null=True,max_length=500)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chart_filters'

class DataSourceFilter(models.Model):
    filter_id = models.AutoField(primary_key=True,db_column='datasource_filter_id')
    user_id = models.IntegerField(db_column='user_id')
    server_id = models.IntegerField(null=True,blank=True)
    file_id = models.IntegerField(null=True,blank=True)
    queryset_id = models.IntegerField(null=True)
    col_name = models.CharField(max_length = 500,null=True)
    data_type = models.CharField(max_length = 500,null=True)
    filter_data = models.TextField(null=True)
    row_data = models.TextField(null=True)
    format_type = models.CharField(null=True,max_length=500)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'datasource_filters'

class functions_tb(models.Model):
    db_id=models.PositiveIntegerField(db_column='database_id')
    function_ip=models.CharField(max_length=1500,db_column='function')
    field_name=models.CharField(max_length=500,db_column='field_name')
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'functions_table'



class charts(models.Model):
    chart_type=models.CharField(max_length=500,null=True)
    min_measures=models.CharField(max_length=500,null=True)
    max_measures=models.CharField(max_length=500,null=True)
    min_dimensions=models.CharField(max_length=500,null=True)
    max_dimensions=models.CharField(max_length=500,null=True)
    min_dates=models.CharField(max_length=500,null=True)
    max_dates=models.CharField(max_length=500,null=True)
    min_geo=models.CharField(max_length=500,null=True)
    max_geo=models.CharField(max_length=500,null=True)

    class Meta:
        db_table = 'charts'

# class DataSourceFilter(models.Model):
#     datasource_filter_id = models.AutoField(primary_key=True,db_column='datasource_filter_id')
#     server_id = models.IntegerField()
#     user_id = models.IntegerField()
#     queryset_id = models.IntegerField()
#     tables = models.CharField(max_length=1000)
#     alias = models.CharField(max_length=1000, default=[])
#     datatype = models.CharField(max_length=1000)
#     columns = models.CharField(max_length=1000)
#     custom_selected_data = models.CharField(max_length=1000)
#     filter_type = models.CharField(max_length=1000)
#     created_at = models.DateTimeField(default=datetime.datetime.now())
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'datasource_filters'




class license_key(models.Model):
    user_id=models.IntegerField()
    key=models.CharField(max_length=1500,db_column='License key')
    max_limit=models.IntegerField()
    is_validated=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'license_keys'


class sheet_data(models.Model):
    id=models.AutoField(db_column='sheet_id',primary_key=True)
    user_id=models.IntegerField()
    chart_id=models.IntegerField()
    server_id = models.IntegerField(null=True,blank=True)
    file_id = models.CharField(max_length=100,null=True,blank=True)
    queryset_id = models.IntegerField()
    filter_ids = models.CharField(max_length=1000,blank=True,null=True)
    sheet_name = models.CharField(max_length=500,null=True,blank=True)
    sheet_filt_id = models.CharField(max_length=1000,blank=True,null=True,db_column='sheetfilter_querysets_id')
    datapath = models.FileField(db_column='sheet_data_path', null=True, blank=True, upload_to='insightapps/sheetdata/',max_length=1000)
    datasrc = models.CharField(max_length=1000,null=True,blank=True,db_column='sheet_data_source')
    sheet_tag_name = models.CharField(max_length=1000,null=True,blank=True,db_column='sheet_tag_name')
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sheet_data'


class grid_type(models.Model):
    id=models.AutoField(primary_key=True)
    grid_type=models.CharField(max_length=100,db_column='grid_type')
    class Meta:
        db_table = 'grid_type'

class dashboard_data(models.Model):
    id=models.AutoField(db_column='dashboard_id',primary_key=True)
    user_id=models.IntegerField()
    server_id = models.CharField(max_length=100,null=True,blank=True)
    queryset_id = models.CharField(max_length=100,null=True,blank=True,default=None,db_column='queryset_id')
    file_id = models.CharField(max_length=100,null=True,blank=True)
    sheet_ids = models.CharField(max_length=1000,blank=True,null=True,db_column='saved_sheet_ids')
    selected_sheet_ids = models.CharField(max_length=1000,blank=True,null=True,db_column='selected_sheet_ids')
    height = models.CharField(max_length=100,null=True,blank=True)
    width = models.CharField(max_length=100,null=True,blank=True)
    grid_id = models.IntegerField(null=True,blank=True)
    role_ids = models.CharField(max_length=100,null=True,blank=True)
    user_ids = models.CharField(max_length=1000,blank=True,null=True)
    dashboard_name = models.CharField(max_length=500,null=True,blank=True)
    datapath = models.FileField(db_column='dashboard_data_path', null=True, blank=True, upload_to='insightapps/dashboard/',max_length=1000)
    datasrc = models.CharField(max_length=1000,null=True,blank=True,db_column='dashboard_data_source')
    imagepath = models.FileField(db_column='dashboard_image_path', null=True, blank=True, upload_to='insightapps/dashboard/images/',max_length=1000)
    imagesrc = models.CharField(max_length=1000,null=True,blank=True,db_column='dashboard_image_source')
    dashboard_tag_name = models.CharField(max_length=1000,null=True,blank=True,db_column='dashboard_tag_name')
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dashboard_data'


class SheetFilter_querysets(models.Model):
    Sheetqueryset_id = models.AutoField(primary_key=True)
    datasource_querysetid = models.IntegerField(null=True,blank=True)
    queryset_id  = models.IntegerField(null=True,blank=True)
    user_id = models.IntegerField(db_column='user_id')
    server_id = models.IntegerField(null=True,blank=True)
    file_id = models.IntegerField(null=True,blank=True)
    filter_id_list = models.TextField(null=True,blank=True)
    columns = models.TextField(null=True,blank=True)
    rows = models.TextField(null=True,blank=True)
    custom_query = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sheetFilter_querysets'



class DashboardFilters(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    dashboard_id = models.IntegerField(null=True,blank=True)
    sheet_id_list = models.CharField(max_length=200,null=True,blank=True)
    filter_name = models.CharField(max_length=200,null=True)
    column_name = models.CharField(max_length=200,null=True)
    column_datatype = models.CharField(max_length=200,null=True)
    queryset_id = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dashboard_filters'

