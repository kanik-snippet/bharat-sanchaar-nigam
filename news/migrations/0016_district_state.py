# Generated by Django 5.1.7 on 2025-03-16 09:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0015_remove_ward_janta_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='state',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='news.state'),
            preserve_default=False,
        ),
    ]
