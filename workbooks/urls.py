from django.urls import path

from . import views


app_name = 'workbooks'


urlpatterns = [
    path('', views.WorkbookListView.as_view(), name='list'),
    path('trainings/<str:training_id>/question', views.WorkbookTrainingQuestionView.as_view(), name='training_question'),
    path('trainings/<str:training_id>/selections/<str:selection_id>', views.WorkbookTrainingAnswerView.as_view(), name='training_answer'),
    path('trainings/<str:training_id>/', views.WorkbookTrainingResultView.as_view(), name='training_result'),
    path('<str:workbook_id>/', views.WorkbookDetailView.as_view(), name='detail'),
]