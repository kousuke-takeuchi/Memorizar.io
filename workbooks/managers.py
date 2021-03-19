import math

from django.db.models import Sum, Count, Case, When, Value

from lib.managers import BaseManager


class WorkbookManager(BaseManager):
    def aggregate_training(self, **kwargs):
        from . import models

        querysets = self.filter(**kwargs)
        workbooks = models.TrainingSelection.objects.filter(training__workbook__in=querysets).select_related().values('training__workbook__title', 'training__workbook__workbook_id', 'correct').order_by('-training__workbook__created_at').annotate(true_count=Count(Case(When(correct=True, then=Value(1)))), selection_count=Count('correct'), training_count=Count('training')).order_by('training__workbook__workbook_id')
        for workbook in workbooks:
            true_rate = math.floor(100 * workbook['true_count'] / workbook['selection_count'])
            workbook['true_rate'] = true_rate
        return workbooks


class ChapterManager(BaseManager):
    pass


class QuestionManager(BaseManager):
    pass


class AnswerManager(BaseManager):
    pass


class RelationshipManager(BaseManager):
    pass


class TrainingManager(BaseManager):
    pass


class TrainingSelectionManager(BaseManager):
    pass

