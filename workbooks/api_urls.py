from django.urls import path

from . import api_views as views


app_name = 'workbooks_api'


urlpatterns = [
    path('', views.WorkbookListView.as_view(), name='list'),
    path('<str:workbook_id>/', views.WorkbookDetailView.as_view(), name='detail'),
]