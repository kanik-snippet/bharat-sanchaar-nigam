# Generated by Django 5.1.7 on 2025-03-15 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_alter_ward_city_village'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cityvillage',
            old_name='p_o',
            new_name='post_office',
        ),
    ]
