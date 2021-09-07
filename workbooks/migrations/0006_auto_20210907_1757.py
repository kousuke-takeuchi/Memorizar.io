# Generated by Django 3.0.5 on 2021-09-07 08:57

from django.db import migrations, models
import django.db.models.deletion
import livefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('workbooks', '0005_training_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='training_type',
            field=models.TextField(choices=[('RAND', 'Random'), ('CHAP', 'Select Chapter')], default='RAND', max_length=4, verbose_name='実施種別'),
        ),
        migrations.CreateModel(
            name='TrainingChapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('live', livefield.fields.LiveField(blank=True, default=True, null=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbooks.Chapter')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbooks.Training')),
            ],
            options={
                'verbose_name': 'training_chapters',
                'verbose_name_plural': 'TrainingChapter',
            },
        ),
        migrations.AddField(
            model_name='training',
            name='chapters',
            field=models.ManyToManyField(through='workbooks.TrainingChapter', to='workbooks.Chapter'),
        ),
    ]
