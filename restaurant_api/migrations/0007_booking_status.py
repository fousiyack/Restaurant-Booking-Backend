# Generated by Django 4.2.2 on 2023-07-24 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_api', '0006_alter_complaint_restaurantid'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(default='pending', max_length=100),
        ),
    ]