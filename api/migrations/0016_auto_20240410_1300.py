# Generated by Django 3.2.23 on 2024-04-10 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_customer_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleDetailsProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tax', models.DecimalField(decimal_places=2, default=18, max_digits=5, verbose_name='impuesto')),
                ('total_item_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='total del ítem')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.sale')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
    ]
