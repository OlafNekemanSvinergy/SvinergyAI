# Generated by Django 3.2.5 on 2022-08-04 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ApiKeys',
            new_name='ApiKey',
        ),
    ]
