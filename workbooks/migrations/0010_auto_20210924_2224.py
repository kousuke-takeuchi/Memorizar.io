# Generated by Django 3.0.5 on 2021-09-24 13:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('workbooks', '0009_auto_20210909_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_id',
            field=models.CharField(db_index=True, default=uuid.uuid4, max_length=100, unique=True, verbose_name='問題識別子'),
        ),
    ]
