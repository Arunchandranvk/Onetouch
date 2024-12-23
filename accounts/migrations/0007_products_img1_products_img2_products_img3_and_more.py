# Generated by Django 5.1.4 on 2024-12-13 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_products_offer_price_alter_products_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='img1',
            field=models.FileField(null=True, upload_to='products'),
        ),
        migrations.AddField(
            model_name='products',
            name='img2',
            field=models.FileField(null=True, upload_to='products'),
        ),
        migrations.AddField(
            model_name='products',
            name='img3',
            field=models.FileField(null=True, upload_to='products'),
        ),
        migrations.AddField(
            model_name='products',
            name='img4',
            field=models.FileField(null=True, upload_to='products'),
        ),
        migrations.AddField(
            model_name='products',
            name='img5',
            field=models.FileField(null=True, upload_to='products'),
        ),
        migrations.AlterField(
            model_name='categories',
            name='category_image',
            field=models.FileField(upload_to='Category Images'),
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]