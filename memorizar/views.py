import datetime

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.conf import settings

from workbooks.models import Training, TrainingSelection


class DashboardView(View):
    template_name = 'memorizar/index.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        
        # 最近7日の1日ごとの学習回数と正解数を集計
        learning_counts = []
        correct_counts = []
        today = datetime.date.today()
        dates = [today - datetime.timedelta(days=i) for i in range(6, -1, -1)]
        for date in dates:
            trainings = Training.objects.filter(created_at__range=[datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max)])
            learning_count = TrainingSelection.objects.filter(training__in=trainings).distinct('training').count()
            correct_count = TrainingSelection.objects.filter(training__in=trainings, correct=True).count()
            learning_counts.append(learning_count)
            correct_counts.append(correct_count)
        weeks = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        dates = [weeks[date.weekday()] for date in dates]
        
        context = dict(dates=dates, learning_counts=learning_counts, correct_counts=correct_counts)
        return render(request, self.template_name, context)