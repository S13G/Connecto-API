# Generated by Django 4.1 on 2022-09-16 00:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0002_remove_equipmentchoice_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journey',
            name='equipment_choice',
        ),
    ]
