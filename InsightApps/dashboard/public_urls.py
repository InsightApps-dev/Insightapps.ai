from django.urls import path
from dashboard import authentication,Connections,columns_extract,views,files,roles,views,dashboard_filter_apis


urlpatterns = [
    path('dashboardretrieve/',Connections.dashboard_retrieve.as_view(),name='Dashboard data retrieve'),
    path('dashboard_columndata_preview/',dashboard_filter_apis.DashboardFilterColumnDataPreview.as_view(),name='Dashboard column Data'),
    path('dashboard_filter_list/',dashboard_filter_apis.Dashboard_filters_list.as_view(),name='dashboard filter list'),
    path('dashboard_filtered_data/',dashboard_filter_apis.FinalDashboardFilterData.as_view(),name='Final Dashboard Filter'),
]