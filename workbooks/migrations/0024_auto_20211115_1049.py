# Generated by Django 3.0.5 on 2021-11-15 01:49

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workbooks', '0023_auto_20211114_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='commentary_image_urls',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, default=list, size=10),
        ),
        migrations.CreateModel(
            name='FlashCardDeck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('title', models.CharField(db_index=True, max_length=250, verbose_name='タイトル')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'flash_card_decks',
                'verbose_name_plural': 'FlashCardDeck',
            },
        ),
        migrations.CreateModel(
            name='FlashCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('front_sentense', models.TextField(verbose_name='表')),
                ('back_sentense', models.TextField(verbose_name='裏')),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbooks.FlashCardDeck')),
            ],
            options={
                'verbose_name': 'flash_cards',
                'verbose_name_plural': 'FlashCard',
            },
        ),
    ]
