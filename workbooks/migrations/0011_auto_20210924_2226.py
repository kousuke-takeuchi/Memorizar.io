# Generated by Django 3.0.5 on 2021-09-24 13:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('workbooks', '0010_auto_20210924_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='chapter_id',
            field=models.CharField(db_index=True, default=uuid.uuid4, max_length=100, verbose_name='章識別子'),
        ),
    ]
