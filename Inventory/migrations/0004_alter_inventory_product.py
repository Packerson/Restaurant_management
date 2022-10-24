# Generated by Django 4.1.2 on 2022-10-24 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0003_remove_inventory_invoice_alter_inventory_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.product', unique=True),
        ),
    ]
