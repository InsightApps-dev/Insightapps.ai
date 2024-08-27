from rest_framework import serializers
from project.settings import perpage

class register_serializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()
    conformpassword=serializers.CharField()
    role=serializers.CharField(allow_null=True,default='',allow_blank=True)


class adding_user_serializer(serializers.Serializer):
    firstname=serializers.CharField()
    lastname=serializers.CharField()
    username=serializers.CharField()
    email=serializers.EmailField()
    is_active=serializers.BooleanField(default=False)
    password=serializers.CharField()
    conformpassword=serializers.CharField()
    # role=serializers.CharField()
    role=serializers.ListField()


class update_user_serializer(serializers.Serializer):
    firstname=serializers.CharField()
    lastname=serializers.CharField()
    username=serializers.CharField()
    email=serializers.EmailField()
    is_active=serializers.BooleanField(default=False)
    role=serializers.ListField()


class activation_serializer(serializers.Serializer):
    otp = serializers.IntegerField()

class previlage_seri(serializers.Serializer):
    role=serializers.CharField()
    previlage_list=serializers.ListField()

class user_edit_role(serializers.Serializer):
    role=serializers.CharField()
    previlage_list=serializers.ListField()

class prev_list_seri(serializers.Serializer):
    previlage_list=serializers.ListField()

class license_serializer(serializers.Serializer):
    key = serializers.CharField()

class sheet_save_serializer(serializers.Serializer):
    sheet_name=serializers.CharField()
    sheet_tag_name=serializers.CharField(allow_null=True,default='',allow_blank=True)
    data = serializers.JSONField(default='')
    chart_id=serializers.CharField()
    queryset_id=serializers.CharField()
    server_id=serializers.CharField(allow_blank=True,allow_null=True,default='')
    file_id = serializers.CharField(allow_blank=True,allow_null=True,default='')
    sheetfilter_querysets_id=serializers.CharField(default='')
    filterId=serializers.ListField(default='')

class sheet_retrieve_serializer(serializers.Serializer):
    # sheet_name=serializers.CharField()  
    queryset_id=serializers.CharField()
    server_id=serializers.CharField(allow_blank=True,allow_null=True,default='')
    file_id = serializers.CharField(allow_blank=True,allow_null=True,default='')

class sheet_name_update_serializer(serializers.Serializer):
    old_sheet_name=serializers.CharField()
    new_sheet_name=serializers.CharField()
    queryset_id=serializers.CharField()
    server_id=serializers.CharField()
    
class dashboard(serializers.Serializer):
    dashboard_tag_name=serializers.CharField(allow_null=True,default='',allow_blank=True)
    queryset_id=serializers.ListField()
    server_id=serializers.ListField(required=False, allow_null=True,default='')
    file_id = serializers.ListField(required=False, allow_null=True,default='')
    sheet_ids=serializers.ListField()
    role_ids=serializers.ListField(required=False, allow_null=True,default='')
    user_ids=serializers.ListField(required=False, allow_null=True,default='')
    dashboard_name=serializers.CharField()
    grid=serializers.CharField(default='scroll')
    height=serializers.CharField()
    width=serializers.CharField()
    selected_sheet_ids=serializers.ListField()
    data=serializers.JSONField()


class role_seri(serializers.Serializer):
    role_name=serializers.CharField()
    role_description=serializers.CharField(allow_null=True,default='',allow_blank=True)
    previlages=serializers.ListField()

class dashboard_image(serializers.Serializer):
    dashboard_id=serializers.CharField()
    imagepath=serializers.ImageField(default='')

class dashboard_retrieve_serializer(serializers.Serializer):
    dashboard_id=serializers.CharField()

class dashboard_name_update_serializer(serializers.Serializer):
    old_dashboard_name=serializers.CharField()
    new_dashboard_name=serializers.CharField()
    queryset_id=serializers.CharField()
    server_id=serializers.CharField()


class dashboard_sheet_update(serializers.Serializer):
    sheet_ids=serializers.ListField()
    dashboard_id=serializers.IntegerField()

class charts_fetch_qr(serializers.Serializer):
    queryset_id=serializers.CharField(default='')
    server_id=serializers.CharField(allow_blank=True,allow_null=True,default='')
    file_id = serializers.CharField(allow_blank=True,allow_null=True,default='')
    search=serializers.CharField(default='')
    page_no=serializers.CharField(default=1)
    page_count=serializers.CharField(default=perpage)

class multiple_charts_data(serializers.Serializer):
    server_data=serializers.ListField()
    files_data=serializers.ListField()

    
class login_serializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ConfirmPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255)
    confirmPassword = serializers.CharField(max_length =255)

class UpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

class name_update_serializer(serializers.Serializer):
    username=serializers.CharField(default='')
    
class DataBaseConnectionSerializer(serializers.Serializer):
    database_type = serializers.CharField()
    hostname = serializers.CharField(default='')
    port = serializers.IntegerField(default=None)
    username = serializers.CharField(default='',allow_null=True,allow_blank=True)
    password = serializers.CharField(default='',allow_null=True,allow_blank=True)
    database = serializers.CharField(default='')
    display_name = serializers.CharField(default='')
    service_name = serializers.CharField(default='')
    path=serializers.FileField(default='')
    database_id = serializers.IntegerField(default=None)
    

class GetColumnFromTableSerializer(serializers.Serializer):
    database_id = serializers.CharField()
    tables = serializers.ListField()
    condition = serializers.ListField(default=[])
    # datatype = serializers.CharField(default='')

    # def validate_tables(self, value):
    #     return value.split(',')

class UploadFileSerializer(serializers.Serializer):
    file_type = serializers.CharField()
    file_path = serializers.FileField()
    
class GenerateReportSerializer(serializers.Serializer):
    db_url = serializers.CharField()
    tables = serializers.CharField()
    # columns = serializers.CharField()
    chart_type = serializers.CharField()
    x_axis = serializers.CharField()
    y_axis = serializers.CharField()

    # def validate_tables(self, value):
    #     return value.split(',')
    
class JoinTableSerializer(serializers.Serializer):
    db_url = serializers.CharField()
    table1 = serializers.CharField()
    table2 = serializers.CharField()
    column1 = serializers.CharField()
    column2 = serializers.CharField()
    operator = serializers.CharField()


# class db_disconnection(serializers.Serializer):
#     server=serializers.CharField()
#     database=serializers.CharField(default='')
#     service_name=serializers.CharField(default='')

class table_input(serializers.Serializer):
    db_id=serializers.IntegerField()
    table_name=serializers.ListField(default='')
    schema=serializers.ListField(default='')
    queryset_id=serializers.IntegerField(default='')

class new_table_input(serializers.Serializer):
    db_id=serializers.IntegerField(allow_null=True,default =None)
    queryset_id=serializers.IntegerField()
    file_id = serializers.CharField(allow_blank=True,allow_null=True,default='')

    
class table_column_input(serializers.Serializer):
    db_id=serializers.IntegerField()
    schema=serializers.ListField()
    table_name=serializers.ListField()
    column_name=serializers.ListField()

class tablejoinserializer(serializers.Serializer):
    query_set_id = serializers.IntegerField(allow_null=True,default = 0)
    database_id = serializers.IntegerField(allow_null=True,default = None)
    joining_tables = serializers.ListField()
    join_type = serializers.ListField()
    joining_conditions = serializers.ListField()
    # query_name = serializers.CharField(allow_null=True,default='')
    file_id = serializers.IntegerField(allow_null=True,default =None)
    dragged_array = serializers.JSONField(allow_null= True,default=None)

class queryserializer(serializers.Serializer):
    database_id= serializers.IntegerField(allow_null=True,default=None)
    file_id = serializers.IntegerField(allow_null=True,default =None)
    query_id= serializers.CharField()
    row_limit = serializers.IntegerField(allow_null=True,default=100)
    datasource_queryset_id  = serializers.CharField(allow_null=True,default =None)



class GetTableInputSerializer(serializers.Serializer):
    table_1 = serializers.DictField()
    database_id = serializers.IntegerField()


class calculated_field(serializers.Serializer):
    db_id=serializers.IntegerField()
    field_name=serializers.CharField(default='calculation')
    function=serializers.CharField()


class CustomSQLSerializer(serializers.Serializer):
    row_limit = serializers.IntegerField(allow_null=True,default=100)
    queryset_id = serializers.CharField(default='')
    database_id = serializers.IntegerField(allow_null=True,default=None)
    file_id = serializers.IntegerField(allow_null=True,default=None)
    custom_query = serializers.CharField(default='')
    query_name = serializers.CharField(allow_null=True,default='')


class queryset_id_sheets(serializers.Serializer):
    queryset_id=serializers.CharField(allow_null=True,default=None)
    search = serializers.CharField(default='')
    page_no = serializers.CharField(default=1)
    page_count = serializers.CharField(default=perpage)


class query_save_serializer(serializers.Serializer):
    query_set_id = serializers.IntegerField()
    # custom_query = serializers.CharField(allow_null=True,default=None)
    database_id = serializers.IntegerField(allow_null=True,default=None)
    file_id = serializers.IntegerField(allow_null=True,default=None)
    query_name = serializers.CharField()


class FilterSerializer(serializers.Serializer):
    type_of_filter = serializers.CharField()
    database_id = serializers.IntegerField(allow_null=True,default=None)
    file_id = serializers.IntegerField(allow_null=True,default=None)
    query_set_id =serializers.IntegerField()
    datasource_queryset_id  = serializers.CharField(allow_null=True,default = None)
    # schema = serializers.CharField()
    # table_name = serializers.CharField()
    # alias = serializers.CharField(default=None)
    col_name = serializers.CharField() 
    data_type = serializers.CharField()
    format_date = serializers.CharField(allow_blank=True,default= 'month/day/year')


# class dimensionserializer(serializers.Serializer):
#     filter_id = serializers.IntegerField()
#     database_id = serializers.IntegerField()
#     queryset_id = serializers.IntegerField()
#     selectd_values = serializers.ListField()

class chartfilter_update_serializer(serializers.Serializer):
    type_of_filter = serializers.CharField()
    filter_id = serializers.IntegerField(allow_null = True,default = None)
    database_id = serializers.IntegerField(allow_null=True,default=None)
    file_id = serializers.IntegerField(allow_null=True,default=None)
    queryset_id = serializers.IntegerField()
    datasource_querysetid = serializers.IntegerField(allow_null = True,default = None)
    range_values = serializers.ListField(allow_null = True,default =[0,0])
    select_values = serializers.ListField()
    col_name = serializers.CharField() 
    data_type = serializers.CharField()
    format_date = serializers.CharField(allow_blank=True,default= 'month/day/year')

class chartfilter_get_serializer(serializers.Serializer):
    type_of_filter = serializers.CharField()
    filter_id = serializers.IntegerField()
    database_id = serializers.IntegerField()
    
   
  

class GetTableInputSerializer11(serializers.Serializer):
    # schema = serializers.CharField()
    # table_name = serializers.CharField()
    # type_of_source = serializers.CharField()
    col = serializers.ListField()
    row = serializers.ListField()
    queryset_id  = serializers.IntegerField()
    datasource_querysetid = serializers.IntegerField(allow_null = True,default = None)
    sheetfilter_querysets_id = serializers.IntegerField(allow_null = True,default = None)
    filter_id = serializers.ListField()
    database_id = serializers.IntegerField(allow_null=True,default=None)
    file_id = serializers.IntegerField(allow_null=True,default=None)

class GetTableInputSerializer22(serializers.Serializer):
    # schema = serializers.CharField()
    # table_name = serializers.CharField()
    # type_of_source = serializers.CharField()
    queryset_id  = serializers.IntegerField()
    datasource_queryset_id = serializers.IntegerField(allow_null = True)
    filter_id = serializers.ListField()
    database_id = serializers.IntegerField(allow_null=True,default=None)
    file_id = serializers.IntegerField(allow_null=True,default=None)

class MeasureInputSerializer(serializers.Serializer):
    database_id = serializers.IntegerField()
    table_1 = serializers.DictField()




class show_me_input(serializers.Serializer):
    db_id=serializers.IntegerField(allow_null=True,default=None)
    col = serializers.ListField()
    row = serializers.ListField()


class alias_serializer(serializers.Serializer):
    tables_list = serializers.ListField()


class Datasource_preview_serializer(serializers.Serializer):
    database_id = serializers.IntegerField()
    query_set_id =serializers.IntegerField()
    tables =serializers.CharField()
    columns = serializers.CharField()
    # data_type = serializers.CharField()
    # format1 = serializers.CharField()

class Datasource_filter_Serializer(serializers.Serializer):
    database_id = serializers.IntegerField()
    query_set_id =serializers.IntegerField()
    tables =serializers.ListField()
    alias = serializers.ListField(default=[])
    columns = serializers.ListField()
    data_type  = serializers.ListField()
    input_list = serializers.ListField()
    format = serializers.ListField()
    

class search_serializer(serializers.Serializer):
    search = serializers.CharField(default='')
    page_no = serializers.CharField(default=1)
    page_count = serializers.CharField(default=perpage)

    
class sheets_list_seri(serializers.Serializer):
    sheet_ids=serializers.ListField(allow_null=True,default='')
    search = serializers.CharField(default='')
    page_no = serializers.CharField(default=1)
    page_count = serializers.CharField(default=perpage)


class sheets_list_serializer(serializers.Serializer):
    sheet_ids=serializers.ListField()


class roles_list_seri(serializers.Serializer):
    role_ids=serializers.ListField()


class dash_prop_update(serializers.Serializer):
    dashboard_id=serializers.IntegerField()
    role_ids=serializers.ListField()
    user_ids=serializers.ListField()


class SearchFilterSerializer(serializers.Serializer):
    querySetId=serializers.IntegerField(allow_null=True,default=None)
    search = serializers.CharField(default='')
    page_no = serializers.CharField(default=1)
    page_count = serializers.CharField(default=perpage)

class list_filters(serializers.Serializer):
    type_of_filter = serializers.CharField(max_length = 200)
    database_id = serializers.IntegerField(allow_null=True,default=None)
    file_id = serializers.IntegerField(allow_null=True,default=None)
    query_set_id =serializers.IntegerField()

class datasource_retrieve(serializers.Serializer):
    database_id = serializers.IntegerField()
    query_set_id =serializers.IntegerField()

class get_table_names(serializers.Serializer):
    database_id = serializers.IntegerField(allow_null=True,default=None)
    file_id = serializers.IntegerField(allow_null=True,default=None)
    query_set_id =serializers.IntegerField()
class GetDataSourceFilter(serializers.Serializer):
    type_filter = serializers.CharField()
    # database_id = serializers.IntegerField()
    filter_id = serializers.IntegerField()

class tables_delete(serializers.Serializer):
    tables_list = serializers.ListField()
    conditions_list = serializers.ListField()
    delete_table = serializers.ListField()

class conditions_delete(serializers.Serializer):
    
    conditions_list = serializers.ListField()
    delete_condition = serializers.CharField()


class rename_serializer(serializers.Serializer):
    database_id = serializers.IntegerField(allow_null=True,default=None)
    file_id = serializers.IntegerField(allow_null=True,default=None)
    queryset_id = serializers.IntegerField()
    old_col_name = serializers.CharField()
    new_col_name = serializers.CharField()

class dashboard_ntfy_stmt(serializers.Serializer):
    database_id = serializers.IntegerField(allow_null=True,default=None)
    file_id = serializers.IntegerField(allow_null=True,default=None)

class sheet_ntfy_stmt(serializers.Serializer):
    sheet_id = serializers.IntegerField()

class query_ntfy_stmt(serializers.Serializer):
    queryset_id = serializers.IntegerField()


class SheetDataSerializer(serializers.Serializer):
    id = serializers.ListField()
    input_list = serializers.ListField()
 

class DashboardpreviewSerializer(serializers.Serializer):
    dashboard_id = serializers.IntegerField()
    queryset_id = serializers.IntegerField()


class Dashboard_datapreviewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    search = serializers.CharField(default='',allow_blank=True)

class Dashboardfilter_save(serializers.Serializer):
    dashboard_filter_id = serializers.IntegerField(default=0,allow_null=True)
    dashboard_id = serializers.IntegerField()
    filter_name = serializers.CharField()
    column = serializers.CharField()
    datatype = serializers.CharField()
    queryset_id = serializers.IntegerField()
    sheets = serializers.ListField(default = [])

class UserInputSerializer(serializers.Serializer):
    sheet_id = serializers.IntegerField()

class dashboard_filter_list(serializers.Serializer):
    dashboard_id = serializers.IntegerField()

class dashboard_filter_applied(serializers.Serializer):
    filter_id = serializers.IntegerField()


class dashboard_querysetname_preview(serializers.Serializer):
    dashboard_id = serializers.IntegerField()

class dashboard_nosheet_data(serializers.Serializer):
    dashboard_id = serializers.IntegerField()
    sheet_ids = serializers.ListField()


class test_data(serializers.Serializer):
    search = serializers.CharField()
