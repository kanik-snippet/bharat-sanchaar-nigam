# Generated by Django 5.1.7 on 2025-03-16 09:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0016_district_state'),
        ('users', '0004_user_ward'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='janta_members', to='news.ward'),
        ),
    ]
