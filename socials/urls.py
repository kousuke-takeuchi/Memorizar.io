from django.conf.urls import url
from django.urls import path

from . import views


app_name = 'socials'


urlpatterns = [
    path('search/', views.WorkbookSearchView.as_view(), name='search'),
    path('<str:workbook_id>/', views.WorkbookDetailView.as_view(), name='detail'),
    path('<str:workbook_id>/register/', views.WorkbookRegistrationView.as_view(), name='register'),
]