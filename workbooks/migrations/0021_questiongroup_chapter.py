# Generated by Django 3.0.5 on 2021-11-10 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workbooks', '0020_workbook_default_answer_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='questiongroup',
            name='chapter',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='workbooks.Chapter'),
        ),
    ]
