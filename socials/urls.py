from django.conf.urls import url
from django.urls import path

from . import views


app_name = 'socials'


urlpatterns = [
    path('search', views.WorkbookSearchView.as_view(), name='search'),
]