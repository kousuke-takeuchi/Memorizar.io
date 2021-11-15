from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from . import models


@admin.register(models.FlashCardDeck)
class FlashCardDeckAdmin(ImportExportModelAdmin):
    date_heirarchy = (
        'updated_at',
    )
    list_display = (
        'user',
        'title',
    )
    search_fields = (
        'created_at',
    )


@admin.register(models.FlashCard)
class FlashCardAdmin(ImportExportModelAdmin):
    date_heirarchy = (
        'updated_at',
    )
    list_display = (
        'deck',
        'front_sentense',
        'back_sentense',
    )
    search_fields = (
        'created_at',
    )