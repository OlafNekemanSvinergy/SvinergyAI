# Generated by Django 3.2.5 on 2022-08-07 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heat_pump', '0010_auto_20220806_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='heatpump',
            name='device_id',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='heatpump',
            name='serial_number',
            field=models.CharField(default='unknown', max_length=200),
            preserve_default=False,
        ),
    ]
