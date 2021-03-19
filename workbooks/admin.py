from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from . import models


@admin.register(models.Workbook)
class WorkbookAdmin(ImportExportModelAdmin):
    date_heirarchy = (
        'updated_at',
    )
    list_display = (
        'workbook_id',
        'user',
        'title',
        'description',
    )
    search_fields = (
        'created_at',
    )


@admin.register(models.Chapter)
class ChapterAdmin(ImportExportModelAdmin):
    date_heirarchy = (
        'updated_at',
    )
    list_display = (
        'chapter_id',
        'workbook',
        'title',
        'description',
    )
    search_fields = (
        'created_at',
    )


@admin.register(models.Question)
class QuestionAdmin(ImportExportModelAdmin):
    date_heirarchy = (
        'updated_at',
    )
    list_display = (
        'question_id',
        'workbook',
        'chapter',
        'title',
        'sentense',
        'image_urls',
        'hint',
        'commentary',
    )
    search_fields = (
        'created_at',
    )


@admin.register(models.Answer)
class AnswerAdmin(ImportExportModelAdmin):
    date_heirarchy = (
        'updated_at',
    )
    list_display = (
        'answer_id', 
        'question', 
        'title', 
        'sentense', 
        'is_true', 
    )
    search_fields = (
        'created_at',
    )


@admin.register(models.Relationship)
class RelationshipAdmin(ImportExportModelAdmin):
    date_heirarchy = (
        'updated_at',
    )
    list_display = (
        'relationship_id',
        'question1',
        'question2',
    )
    search_fields = (
        'created_at',
    )


@admin.register(models.Training)
class TrainingAdmin(ImportExportModelAdmin):
    date_heirarchy = (
        'updated_at',
    )
    list_display = (
        'training_id',
        'user',
        'workbook',
        'done',
    )
    search_fields = (
        'created_at',
    )


@admin.register(models.TrainingSelection)
class TrainingSelectionAdmin(ImportExportModelAdmin):
    date_heirarchy = (
        'updated_at',
    )
    list_display = (
        'training_selection_id',
        'training',
        'question',
        'answer',
        'correct',
        'duration',
    )
    search_fields = (
        'created_at',
    )