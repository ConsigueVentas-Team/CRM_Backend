# Generated by Django 3.2.23 on 2024-01-11 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_user_id_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('clientID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=40)),
                ('documentType', models.CharField(choices=[(0, 'DNI'), (1, 'Cedula'), (2, 'Pasaporte'), (3, 'Otro')], max_length=1)),
                ('documentNumber', models.CharField(max_length=14, unique=True)),
                ('email', models.CharField(max_length=30)),
                ('cellNumber', models.CharField(max_length=12)),
                ('address', models.CharField(max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('saleID', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paymentType', models.CharField(choices=[(0, 'CREDIT_CARD'), (1, 'DEBIT_CARD'), (2, 'CASH'), (3, 'BANK_TRANSFER'), (4, 'OTHER')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.client')),
            ],
        ),
    ]
