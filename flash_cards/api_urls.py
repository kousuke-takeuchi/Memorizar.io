from django.urls import path

from . import api_views as views


app_name = 'flash_cards_api'


urlpatterns = [
    path('', views.FlashCardDeckListView.as_view(), name='list'),
    path('<str:deck_id>/', views.FlashCardDeckDetailView.as_view(), name='detail'),
]