# Generated by Django 3.0.5 on 2021-03-05 05:05

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import livefield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('live', livefield.fields.LiveField(blank=True, default=True, null=True)),
                ('answer_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True, verbose_name='答えID')),
                ('title', models.CharField(db_index=True, max_length=250, verbose_name='タイトル')),
                ('sentense', models.TextField(verbose_name='問題文')),
                ('is_true', models.BooleanField(default=False, verbose_name='正しい選択肢かどうか')),
            ],
            options={
                'verbose_name': 'answers',
                'verbose_name_plural': 'Answer',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('live', livefield.fields.LiveField(blank=True, default=True, null=True)),
                ('question_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True, verbose_name='問題識別子')),
                ('title', models.CharField(db_index=True, max_length=250, verbose_name='タイトル')),
                ('sentense', models.TextField(verbose_name='問題文')),
                ('image_urls', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), size=10)),
                ('hint', models.TextField(blank=True, default=None, null=True, verbose_name='問題ヒント文章')),
                ('commentary', models.TextField(blank=True, default=None, null=True, verbose_name='正解解説文章')),
            ],
            options={
                'verbose_name': 'questions',
                'verbose_name_plural': 'Question',
            },
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('live', livefield.fields.LiveField(blank=True, default=True, null=True)),
                ('training_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True, verbose_name='イベントID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'trainings',
                'verbose_name_plural': 'Training',
            },
        ),
        migrations.CreateModel(
            name='Workbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('live', livefield.fields.LiveField(blank=True, default=True, null=True)),
                ('workbook_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True, verbose_name='問題集識別子')),
                ('title', models.CharField(db_index=True, max_length=250, verbose_name='タイトル')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='詳細説明文')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'workbooks',
                'verbose_name_plural': 'Workbook',
            },
        ),
        migrations.CreateModel(
            name='TrainingSelection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('live', livefield.fields.LiveField(blank=True, default=True, null=True)),
                ('training_selection_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True, verbose_name='選択ID')),
                ('correct', models.BooleanField(default=False, verbose_name='正解かどうか')),
                ('duration', models.IntegerField(verbose_name='かかった時間[ms]')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbooks.Answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbooks.Question')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbooks.Training')),
            ],
            options={
                'verbose_name': 'training_selections',
                'verbose_name_plural': 'TrainingSelection',
            },
        ),
        migrations.AddField(
            model_name='training',
            name='workbook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbooks.Workbook'),
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('live', livefield.fields.LiveField(blank=True, default=True, null=True)),
                ('relationship_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True, verbose_name='類似ID')),
                ('question1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question1', to='workbooks.Question')),
                ('question2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question2', to='workbooks.Question')),
            ],
            options={
                'verbose_name': 'relationships',
                'verbose_name_plural': 'Relationship',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='workbook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbooks.Workbook'),
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('live', livefield.fields.LiveField(blank=True, default=True, null=True)),
                ('chapter_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True, verbose_name='章識別子')),
                ('title', models.CharField(db_index=True, max_length=250, verbose_name='タイトル')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='詳細説明文')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbooks.Question')),
                ('workbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbooks.Workbook')),
            ],
            options={
                'verbose_name': 'chapters',
                'verbose_name_plural': 'Chapter',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbooks.Question'),
        ),
    ]
