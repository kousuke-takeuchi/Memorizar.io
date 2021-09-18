import os
from celery import shared_task

from django.contrib.auth.models import User

from . import services


@shared_task
def import_workbook_task(user_id, title, file_path):
    user = User.objects.get(pk=user_id)
    service = services.WorkbookService()
    try:
        service.import_workbook(user, title, file_path)
        # インポートが完了したらメールで通知
        service.notify_success(user, title)
    except Exception as exc:
        # インポートを失敗したらメールで通知
        service.notify_failure(user, title)
        print(exc)
    os.remove(file_path)