# Generated by Django 3.2.6 on 2021-09-13 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_rename_name_product_商品名稱'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='商品名稱',
            new_name='name',
        ),
    ]
