# Generated by Django 5.1.4 on 2024-12-16 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_cart_cartitem_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]