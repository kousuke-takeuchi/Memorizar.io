from django.urls import path

from . import views, api_views


app_name = 'diagnoses'


urlpatterns = [
    # path('upload/', api_views.DiagnosisCreateView.as_view(), name='upload_diagnosis_create'),
]