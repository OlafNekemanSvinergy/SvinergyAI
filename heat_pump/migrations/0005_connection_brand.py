# Generated by Django 3.2.5 on 2022-08-04 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heat_pump', '0004_connection'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='brand',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
    ]
