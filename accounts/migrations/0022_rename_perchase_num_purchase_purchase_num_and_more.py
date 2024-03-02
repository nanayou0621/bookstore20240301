# Generated by Django 5.0 on 2024-01-18 06:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_customuser_address_alter_customuser_cart'),
        ('store', '0002_alter_cartunit_book_alter_cartunit_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='perchase_num',
            new_name='purchase_num',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.cart'),
        ),
    ]
