# Generated by Django 3.0.5 on 2021-11-01 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workbooks', '0014_trainingselection_confident'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('workbook_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True, verbose_name='問題集識別子')),
                ('title', models.CharField(db_index=True, max_length=250, verbose_name='タイトル')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='詳細説明文')),
                ('image_url', models.URLField(blank=True, default=None, null=True, verbose_name='問題集画像')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'categories',
                'verbose_name_plural': 'Category',
            },
        ),
        migrations.AddField(
            model_name='workbook',
            name='image_url',
            field=models.URLField(blank=True, default=None, null=True, verbose_name='問題集画像'),
        ),
        migrations.CreateModel(
            name='WorkbookCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbooks.Category')),
                ('workbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbooks.Workbook')),
            ],
            options={
                'verbose_name': 'workbook_categories',
                'verbose_name_plural': 'WorkbookCategory',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='workbooks',
            field=models.ManyToManyField(through='workbooks.WorkbookCategory', to='workbooks.Workbook'),
        ),
        migrations.AddField(
            model_name='workbook',
            name='categories',
            field=models.ManyToManyField(through='workbooks.WorkbookCategory', to='workbooks.Category'),
        ),
    ]