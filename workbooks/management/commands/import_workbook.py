from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from workbooks.services import WorkbookService

class Command(BaseCommand):
    help = 'Import new workbook from excel'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)
        parser.add_argument('--username', type=str)


    def handle(self, *args, **options):
        filename = options['file']
        username = options['username']

        user = User.objects.get(username=username)
        service = WorkbookService()
        service.import_workbook(user, filename)
        self.stdout.write(self.style.SUCCESS('workbook was imported successfully'))