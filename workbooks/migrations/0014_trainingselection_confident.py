# Generated by Django 3.0.5 on 2021-10-31 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workbooks', '0013_auto_20211023_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingselection',
            name='confident',
            field=models.BooleanField(default=True, verbose_name='迷いがなかったかどうか'),
        ),
    ]
