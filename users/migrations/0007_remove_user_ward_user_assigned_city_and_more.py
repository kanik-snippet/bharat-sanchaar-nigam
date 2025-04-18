# Generated by Django 5.1.7 on 2025-03-19 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0020_alter_cityvillage_chairman_and_more'),
        ('users', '0006_alter_user_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='ward',
        ),
        migrations.AddField(
            model_name='user',
            name='assigned_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_in_city', to='news.cityvillage'),
        ),
        migrations.AddField(
            model_name='user',
            name='assigned_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_in_country', to='news.country'),
        ),
        migrations.AddField(
            model_name='user',
            name='assigned_district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_in_district', to='news.district'),
        ),
        migrations.AddField(
            model_name='user',
            name='assigned_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_in_state', to='news.state'),
        ),
        migrations.AddField(
            model_name='user',
            name='assigned_village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_in_village', to='news.cityvillage'),
        ),
        migrations.AddField(
            model_name='user',
            name='assigned_ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_in_ward', to='news.ward'),
        ),
    ]
