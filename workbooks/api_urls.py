from django.urls import path

from . import api_views as views


app_name = 'workbooks_api'


urlpatterns = [
    path('', views.WorkbookListView.as_view(), name='list'),
    path('upload/', views.FileUploadView.as_view(), name='file_upload'),
    path('<str:workbook_id>/', views.WorkbookDetailView.as_view(), name='detail'),
    path('<str:workbook_id>/chapters/', views.ChapterListView.as_view(), name='chapter_list'),
    path('<str:workbook_id>/chapters/<str:chapter_id>/', views.ChapterDetailView.as_view(), name='chapter_detail'),
    path('<str:workbook_id>/questions/', views.QuestionListView.as_view(), name='quetion_list'),
    path('<str:workbook_id>/question_groups/', views.QuestionGroupListView.as_view(), name='quetion_group_list'),
    path('<str:workbook_id>/question/bulk/', views.QuestionBulkCreateView.as_view(), name='quetion_bulk_create'),
    path('<str:workbook_id>/questions/<str:question_id>/', views.QuestionDetailView.as_view(), name='quetion_detail'),
    path('<str:workbook_id>/questions/<str:question_id>/delete/', views.QuestionDeleteView.as_view(), name='quetion_delete'),
    path('<str:workbook_id>/trainings/', views.TrainingListView.as_view(), name='training_list'),
    path('<str:workbook_id>/trainings/<str:training_id>/questions/', views.TrainingQuestionListView.as_view(), name='training_question_list'),
    path('<str:workbook_id>/trainings/<str:training_id>/selections/', views.TrainingSelectionListView.as_view(), name='training_selection_list'),
]