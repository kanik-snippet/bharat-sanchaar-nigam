# Generated by Django 5.1.7 on 2025-03-15 17:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_ward_ward_member'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cityvillage',
            name='mla',
            field=models.OneToOneField(blank=True, limit_choices_to={'role': 'mla'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_city', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cityvillage',
            name='sarpanch',
            field=models.OneToOneField(blank=True, limit_choices_to={'role': 'sarpanch'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_village', to=settings.AUTH_USER_MODEL),
        ),
    ]
