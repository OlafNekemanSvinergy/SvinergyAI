# Generated by Django 3.2.5 on 2022-08-11 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HeatPump',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('brand', models.CharField(choices=[('Bosch', 'Bosch'), ('Vaillant', 'Vaillant')], max_length=15)),
                ('serial_number', models.CharField(max_length=200, unique=True)),
                ('max_power', models.IntegerField()),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('temp_inside', models.DecimalField(decimal_places=5, max_digits=10)),
                ('temp_target', models.DecimalField(decimal_places=5, max_digits=10)),
                ('temp_range', models.DecimalField(decimal_places=5, max_digits=10)),
                ('temp_outdoor', models.DecimalField(decimal_places=5, max_digits=10)),
                ('heating_on', models.BooleanField()),
                ('power_level', models.DecimalField(decimal_places=5, max_digits=7)),
                ('heat_pump', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heat_pump.heatpump')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('brand', models.CharField(choices=[('Bosch', 'Bosch'), ('Vaillant', 'Vaillant')], max_length=15)),
                ('device_id', models.CharField(max_length=200, unique=True)),
                ('access_token', models.CharField(max_length=2000)),
                ('refresh_token', models.CharField(max_length=2000)),
                ('valid_until', models.DateTimeField()),
                ('expires_in', models.IntegerField()),
                ('active', models.BooleanField(default=False)),
                ('heat_pump', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='heat_pump.heatpump')),
            ],
        ),
    ]
