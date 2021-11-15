from django.conf.urls import url
from django.urls import path

from . import views


app_name = 'flash_cards'


urlpatterns = [
    path('', views.FlashCardDeckListView.as_view(), name='list'),
    path('new/', views.FlashCardDeckCreateView.as_view(), name='create'),
]