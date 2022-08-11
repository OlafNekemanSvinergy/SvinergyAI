# Generated by Django 3.2.5 on 2022-08-11 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heat_pump', '0018_rename_valid_connection_expires_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='token_type',
            field=models.CharField(choices=[('Bearer', 'Bearer'), ('Basic', 'Basic')], default='Bearer', max_length=15),
        ),
    ]