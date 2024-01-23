# Generated by Django 3.2.23 on 2024-01-22 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_category_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='document_type',
            field=models.IntegerField(verbose_name=[(0, 'DNI'), (1, 'CEDULA'), (2, 'PASAPORTE'), (3, 'OTRO')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(default=1, verbose_name=[(1, 'ADMIN'), (2, 'EMPLOYEE')]),
            preserve_default=False,
        ),
    ]