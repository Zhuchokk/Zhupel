# Generated by Django 4.0 on 2022-06-19 15:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_remove_article_dislike_count_article_comment_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='secret_key',
            field=models.CharField(default='none', max_length=32),
        ),
        migrations.AlterField(
            model_name='article',
            name='themes',
            field=models.CharField(default='["без темы"]', max_length=256),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 19, 15, 15, 22, 382658, tzinfo=utc)),
        ),
    ]
