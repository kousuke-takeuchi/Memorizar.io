from django.conf.urls import url
from django.urls import path

from . import views


app_name = 'workbooks'


urlpatterns = [
    path('', views.WorkbookListView.as_view(), name='list'),
    path('new/', views.WorkbookCreateView.as_view(), name='create'),
    path('import/', views.WorkbookImportView.as_view(), name='import'),
    path('<str:workbook_id>/', views.WorkbookDetailView.as_view(), name='detail'),
    path('<str:workbook_id>/edit/', views.WorkbookEditView.as_view(), name='edit'),
    path('<str:workbook_id>/delete/', views.WorkbookDeleteView.as_view(), name='delete'),
    path('<str:workbook_id>/questions/new/', views.QuestionCreateView.as_view(), name='question_new'),
    path('<str:workbook_id>/questions/new_group/', views.QuestionGroupCreateView.as_view(), name='question_group_new'),
    path('<str:workbook_id>/questions/new_scan/', views.QuestionScanView.as_view(), name='question_new_scan'),
    path('<str:workbook_id>/questions/<str:question_id>/edit/', views.QuestionEditView.as_view(), name='question_edit'),
    path('<str:workbook_id>/questions/<str:question_id>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('<str:workbook_id>/chapters/new/', views.ChapterCreateView.as_view(), name='chapter_new'),
    path('<str:workbook_id>/chapters/<str:chapter_id>/edit/', views.ChapterEditView.as_view(), name='chapter_edit'),
    path('<str:workbook_id>/chapters/<str:chapter_id>/delete/', views.ChapterDeleteView.as_view(), name='chapter_delete'),
    path('<str:workbook_id>/trainings/select_chapters', views.WorkbookTrainingSelectChapterView.as_view(), name='training_select_chapter'),
    path('<str:workbook_id>/trainings/<str:training_id>/', views.WorkbookTrainingResultView.as_view(), name='training_result'),
    path('<str:workbook_id>/trainings/<str:training_id>/question/', views.WorkbookTrainingQuestionView.as_view(), name='training_question'),
    path('<str:workbook_id>/trainings/<str:training_id>/selections/<str:selection_id>/', views.WorkbookTrainingAnswerView.as_view(), name='training_answer'),
    path('<str:workbook_id>/wrongs/', views.WorkbookWrongView.as_view(), name='wrongs'),
]