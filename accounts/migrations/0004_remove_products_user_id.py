# Generated by Django 5.1.4 on 2024-12-12 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_product_products_delete_myaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='user_id',
        ),
    ]