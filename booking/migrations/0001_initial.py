# Generated by Django 4.1 on 2022-09-08 09:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pronoun', models.CharField(choices=[('Mr', 'Mr'), ('Mrs', 'Mrs')], max_length=3)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email_address', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('session_key', models.CharField(editable=False, max_length=10000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_ID', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, unique=True)),
                ('route', models.CharField(choices=[('With Return', 'With Return'), ('One Way', 'One Way')], default='With Return', max_length=255)),
                ('departure', models.DateField()),
                ('returning', models.DateField()),
                ('arrival_flight_number', models.CharField(blank=True, max_length=20, null=True)),
                ('landing_time', models.TimeField(default=None)),
                ('drop_off', models.CharField(default=None, max_length=255)),
                ('return_date', models.DateField()),
                ('pickup_time', models.TimeField(default=None)),
                ('pickup_address', models.CharField(default=None, max_length=255)),
                ('departure_flight_number', models.CharField(blank=True, max_length=20, null=True)),
                ('departure_flight_time', models.TimeField(default=None)),
                ('session_key', models.CharField(editable=False, max_length=10000, null=True)),
                ('booker', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='booking.booker')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(5.0, 'Child Seat'), (5.0, 'Infant Seat'), (0, 'Wheelchair'), (5.0, 'Booster Seat'), (10.0, 'Extra Stop in Town'), (5.0, 'Ski and Snowboard'), (10.0, 'Bicycle')], default=None, max_length=255)),
                ('quantity', models.IntegerField(null=True)),
                ('date_created', models.DateTimeField(null=True)),
                ('session_key', models.CharField(editable=False, max_length=10000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_make_and_model', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Economy Van', 'Economy Van'), ('Economy Sedan', 'Economy Sedan'), ('Premium Sedan', 'Premium Sedan'), ('MiniBus', 'MiniBus'), ('Luxury Bus', 'Bus'), ('Limousine', 'Limousine')], max_length=55)),
                ('seats', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('baggage', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('tag', models.CharField(choices=[('TIS', 'Travel in style'), ('SAC', 'Style and comfort'), ('EC', 'Extra Comfort'), ('NAS', 'Not a shuttle')], max_length=255)),
                ('inquiry', models.BooleanField(default=False)),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('old_price', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Airport', 'Airport'), ('Hotel', 'Hotel'), ('Train Station', 'Train Station'), ('City', 'City')], max_length=255)),
                ('code', models.CharField(max_length=4)),
                ('longitude', models.CharField(max_length=255)),
                ('latitude', models.CharField(max_length=255)),
                ('display', models.BooleanField(default=True)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.country')),
            ],
        ),
        migrations.CreateModel(
            name='Journey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_journey_price', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('old_journey_price', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('passengers', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('distance', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('session_key', models.CharField(editable=False, max_length=10000, null=True)),
                ('from_place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='journey_from_place', to='booking.place')),
                ('to_place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.place')),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_item_count', models.IntegerField(default=None)),
                ('return_item_count', models.IntegerField(default=None)),
                ('session_key', models.CharField(editable=False, max_length=10000, null=True)),
                ('booking', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='extras', to='booking.booking')),
                ('equipment', models.ManyToManyField(to='booking.equipmenttype')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='journey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.journey'),
        ),
        migrations.AddField(
            model_name='booking',
            name='place',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='booking.place'),
        ),
        migrations.AddField(
            model_name='booker',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.country'),
        ),
    ]
