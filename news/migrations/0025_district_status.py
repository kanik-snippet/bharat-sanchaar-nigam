# Generated by Django 5.1.7 on 2025-03-29 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0024_alter_ward_status_userlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=10),
        ),
    ]
