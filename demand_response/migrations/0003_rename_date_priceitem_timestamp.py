# Generated by Django 3.2.5 on 2022-08-09 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demand_response', '0002_alter_priceitem_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='priceitem',
            old_name='date',
            new_name='timestamp',
        ),
    ]