# Generated by Django 4.1 on 2022-09-10 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_remove_booking_equipment_journey_equipment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='first_item_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='return_item_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='journey',
            name='equipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.equipment'),
        ),
    ]
