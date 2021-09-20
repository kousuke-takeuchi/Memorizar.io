from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views


app_name = 'users'


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("", include("social_django.urls")),
    path('setting/', views.SettingView.as_view(), name='setting'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page=reverse_lazy('Userauth:login') # you can use your named URL here just like you use the **url** tag in your django template
    ), name='logout'),
]