# Generated by Django 5.1.7 on 2025-03-28 13:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0021_news_is_deleted_alter_news_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='title',
        ),
        migrations.AddField(
            model_name='news',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='news',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='news_photos/'),
        ),
        migrations.AddField(
            model_name='news',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='news_videos/'),
        ),
        migrations.AlterField(
            model_name='news',
            name='city_village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.cityvillage'),
        ),
        migrations.AlterField(
            model_name='news',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.country'),
        ),
        migrations.AlterField(
            model_name='news',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.district'),
        ),
        migrations.AlterField(
            model_name='news',
            name='role',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='news',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.state'),
        ),
        migrations.AlterField(
            model_name='news',
            name='ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.ward'),
        ),
    ]
