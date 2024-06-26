# Generated by Django 3.2.23 on 2024-03-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_image_url_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='products'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
