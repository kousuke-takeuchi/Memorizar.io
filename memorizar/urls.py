"""memorizar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views, api_views


urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
    path('privacy_policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('agreement/', views.AgreementView.as_view(), name='agreement'),
    path('admin/', admin.site.urls),
    path('flash_cards/', include('flash_cards.urls', namespace='flash_cards')),
    path('socials/', include('socials.urls', namespace='socials')),
    path('users/', include('users.urls', namespace='users')),
    path('workbooks/', include('workbooks.urls', namespace='workbooks')),
]

urlpatterns += [
    path('api/upload/', api_views.MediaUploadView.as_view(), name='upload_api'),
    path('api/workbooks/', include('workbooks.api_urls', namespace='workbooks_api')),
    path('api/flash_cards/', include('flash_cards.api_urls', namespace='flash_cards_api')),
]
