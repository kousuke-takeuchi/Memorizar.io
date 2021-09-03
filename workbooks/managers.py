import math

from django.db.models import Sum, Count, Case, When, Value

from lib.managers import BaseManager


class WorkbookManager(BaseManager):
    def aggregate_training(self, **kwargs):
        from . import models

        # querysets = models.TrainingSelection.objects.filter(training__workbook__in=self.filter(**kwargs))
        # querysets = querysets.select_related().values('training__workbook__created_at', 'training__workbook__title', 'training__workbook__workbook_id', 'correct')
        # querysets = querysets.annotate(true_count=Count(Case(When(correct=True, then=Value(1)))), selection_count=Count('correct'), training_count=Count('training'))
        # querysets = querysets.order_by('-training__workbook__created_at')
        
        workbooks = self.filter(**kwargs)
        results = []
        for workbook in workbooks:
            querysets = models.TrainingSelection.objects.filter(training__workbook=workbook)
            querysets = querysets.values('training__workbook')
            querysets = querysets.annotate(true_count=Count(Case(When(correct=True, then=Value(1)))), selection_count=Count('correct'), training_count=Count('training', distinct=True))
            if len(querysets) == 0:
                results.append({
                    'workbook_id': workbook.workbook_id,
                    'title': workbook.title,
                    'created_at': None,
                    'true_count': 0,
                    'selection_count': 0,
                    'true_rate': 0.0,
                    'training_count': 0,
                })
            else:
                start_at = models.Training.objects.filter(workbook=workbook, done=True).first().created_at
                true_rate = math.floor(100 * querysets[0]['true_count'] / querysets[0]['selection_count'])
                results.append({
                    'workbook_id': workbook.workbook_id,
                    'title': workbook.title,
                    'created_at': start_at,
                    'true_count': querysets[0]['true_count'],
                    'selection_count': querysets[0]['selection_count'],
                    'true_rate': true_rate,
                    'training_count': querysets[0]['training_count'],
                })
        return results


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
    def aggregate(self, **kwargs):
        querysets = self.filter(**kwargs)
        querysets = querysets.values('training__created_at')
        querysets = querysets.annotate(true_count=Count(Case(When(correct=True, then=Value(1)))), selection_count=Count('correct'), duration=Sum('duration'))
        querysets = querysets.order_by('-training__created_at')
        for result in querysets:
            result['true_rate'] = math.floor(100 * result['true_count'] / result['selection_count'])
        return querysets

