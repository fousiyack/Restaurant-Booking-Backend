# Generated by Django 4.2.2 on 2023-08-02 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='restaurant',
            new_name='restaurant_id',
        ),
    ]
