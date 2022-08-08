# Generated by Django 3.2.5 on 2022-08-04 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heat_pump', '0003_datapoint'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('api_key', models.CharField(max_length=200)),
                ('refresh_token', models.CharField(max_length=200)),
                ('valid_until', models.DateTimeField()),
                ('valid', models.IntegerField()),
                ('active', models.BooleanField()),
            ],
        ),
    ]