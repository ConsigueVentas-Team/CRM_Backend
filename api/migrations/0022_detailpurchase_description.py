# Generated by Django 3.2.23 on 2024-07-01 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20240621_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailpurchase',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]