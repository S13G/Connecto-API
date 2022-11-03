# Generated by Django 4.1 on 2022-09-18 21:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0008_rename_timestamp_booking_date_filled_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=1000, null=True, unique=True)),
                ('verified', models.BooleanField(default=False, null=True)),
                ('session_key', models.CharField(blank=True, max_length=300, null=True)),
                ('date_paid', models.DateTimeField(default=django.utils.timezone.now)),
                ('booking',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.booking')),
            ],
        ),
    ]
