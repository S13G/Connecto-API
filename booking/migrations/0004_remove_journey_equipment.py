# Generated by Django 4.1 on 2022-09-10 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_remove_booking_equipment_booking_equipment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journey',
            name='equipment',
        ),
    ]
