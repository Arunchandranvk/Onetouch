# Generated by Django 5.1.4 on 2024-12-15 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_appoinment_date_alter_appoinment_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appoinment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Rejected'), ('Rejected', 'Rejected')], default='Pending', max_length=100),
        ),
    ]
