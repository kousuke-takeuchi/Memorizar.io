from django.urls import path

from . import api_views as views


app_name = 'workbooks_api'


urlpatterns = [
    path('', views.WorkbookListView.as_view(), name='list'),
    path('<str:workbook_id>/', views.WorkbookDetailView.as_view(), name='detail'),
    path('<str:workbook_id>/questions/', views.QuestionListView.as_view(), name='quetion_list'),
    path('<str:workbook_id>/questions/<str:question_id>/', views.QuestionDetailView.as_view(), name='quetion_detail'),
]