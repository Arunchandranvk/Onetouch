# Generated by Django 5.1.4 on 2024-12-23 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_remove_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='tax',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='total_payable',
            field=models.FloatField(null=True),
        ),
    ]
