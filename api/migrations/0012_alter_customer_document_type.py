# Generated by Django 3.2.23 on 2024-04-03 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_service_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='document_type',
            field=models.IntegerField(verbose_name=[(0, 'DNI'), (1, 'CEDULA'), (2, 'PASAPORTE'), (3, 'OTRO')]),
        ),
    ]
