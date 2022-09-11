from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from shortuuidfield import ShortUUIDField

import haversine as hs

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=4, null=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name} ({self.code})"


class Place(models.Model):
    PLACES = [
        ('Airport', 'Airport'),
        ('Hotel', 'Hotel'),
        ('Train Station', 'Train Station'),
        ('City', 'City')
    ]
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    category = models.CharField(choices=PLACES, max_length=255)
    code = models.CharField(max_length=10)
    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    display = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Vehicle(models.Model):
    TRAVEL_IN_STYLE = 'TIS'
    STYLE_AND_COMFORT = 'SAC'
    EXTRA_COMFORT = 'EC'
    NOT_A_SHUTTLE = 'NAS'

    TAG_CHOICES = [
        (TRAVEL_IN_STYLE, 'Travel in style'),
        (STYLE_AND_COMFORT, 'Style and comfort'),
        (EXTRA_COMFORT, 'Extra Comfort'),
        (NOT_A_SHUTTLE, 'Not a shuttle'),
    ]

    CATEGORY = [
        ('Economy Van', 'Economy Van'),
        ('Economy Sedan', 'Economy Sedan'),
        ('Premium Sedan', 'Premium Sedan'),
        ('MiniBus', 'MiniBus'),
        ('Luxury Bus', 'Bus'),
        ('Limousine', 'Limousine')
    ]

    vehicle_make_and_model = models.CharField(max_length=255)
    category = models.CharField(max_length=55, choices=CATEGORY)
    seats = models.IntegerField(validators=[MinValueValidator(1)])
    baggage = models.IntegerField(validators=[MinValueValidator(1)])
    tag = models.CharField(max_length=255, choices=TAG_CHOICES)
    inquiry = models.BooleanField(default=False)
    current_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    old_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.vehicle_make_and_model

class EquipmentType(models.Model):
    EQUIPMENT_CHOICE = [
        ('CHILD SEAT', 'Child Seat'),
        ('INFANT SEAT', 'Infant Seat'),
        ('WHEELCHAIR', 'Wheelchair'),
        ('BOOSTER SEAT', 'Booster Seat'),
        ('EXTRA STOP IN TOWN', 'Extra Stop in Town'),
        ('SKIS AND SNOWBOARD', 'Ski and Snowboard'),
        ('BICYCLE', 'Bicycle'),
    ]
    name = models.CharField(max_length=255, choices=EQUIPMENT_CHOICE)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)], null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name}"


class EquipmentChoice(models.Model):
    equipment = models.ForeignKey(EquipmentType, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(validators=[MaxValueValidator(5)])
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)], null=True)
    date_created = models.DateTimeField(default=timezone.now)
    session_key = models.CharField(max_length=10000, null=True, editable=False)

    def save(self, *args, **kwargs):
        self.price = self.equipment.price * self.quantity
        return super(EquipmentChoice, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.equipment}"


class Journey(models.Model):
    from_place = models.ForeignKey(
        Place, on_delete=models.CASCADE, null=True, related_name="journey_from_place")
    to_place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    equipment_choice = models.ManyToManyField(EquipmentChoice)
    current_price = models.DecimalField(
        max_digits=60, decimal_places=2, null=True)
    old_price = models.DecimalField(
        max_digits=60, decimal_places=2, null=True)
    passengers = models.IntegerField(validators=[MinValueValidator(1)])
    distance = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    session_key = models.CharField(max_length=10000, null=True, editable=False)

    @property
    def with_return_current_price(self):
        return float(self.current_price * 2)
    
    @property
    def with_return_old_price(self):
        return float(self.old_price * 2)

    def save(self, *args, **kwargs):
        super(Journey, self).save(*args, **kwargs)
        location1 = (Decimal(self.from_place.latitude), Decimal(self.from_place.longitude))
        location2 = (Decimal(self.to_place.latitude), Decimal(self.to_place.longitude))
        journey_distance = Decimal(hs.haversine(location1, location2))
        self.distance = journey_distance
        old_price_per_km = self.vehicle.old_price * self.passengers
        price_per_km = self.vehicle.current_price * self.passengers
        equipment_sum = [equipment for equipment in self.equipment_choice.all().values_list("price", flat=True)]
        self.current_price = journey_distance * (price_per_km / 1000) + sum(equipment_sum)
        self.old_price = journey_distance * (old_price_per_km / 1000) + sum(equipment_sum)
        return super(Journey, self).save(*args, **kwargs)

    def __str__(self):
        return f"From {self.from_place} to {self.to_place}"


class Booker(models.Model):
    MISTER = 'Mr'
    MRS = 'Mrs'

    PRONOUN = [
        (MISTER, 'Mr'),
        (MRS, 'Mrs')
    ]

    pronoun = models.CharField(max_length=3, choices=PRONOUN)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.EmailField(max_length=254)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=20)
    session_key = models.CharField(max_length=10000, null=True, editable=False)

    def __str__(self):
        return f"{self.pronoun} {self.first_name} {self.last_name}"


class Booking(models.Model):
    ROUTE = (
        ('With Return', 'With Return'),
        ('One Way', 'One Way'),
    )
    reference_ID = ShortUUIDField(
        max_length=5, unique=True, editable=False)
    route = models.CharField(
        max_length=255, choices=ROUTE, default='With Return')
    booker = models.ForeignKey(
        Booker, on_delete=models.CASCADE, related_name="customer", null=True)
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, null=True)
    departure = models.DateField()
    returning = models.DateField()
    arrival_flight_number = models.CharField(
        max_length=20, null=True, blank=True)
    landing_time = models.TimeField(null=True)
    drop_off = models.CharField(max_length=255, null=True)
    return_date = models.DateField()
    pickup_time = models.TimeField(null=True)
    pickup_address = models.CharField(max_length=255, null=True)
    departure_flight_number = models.CharField(
        max_length=20, null=True, blank=True)
    departure_flight_time = models.TimeField(null=True)
    session_key = models.CharField(max_length=10000, null=True, editable=False)

    def __str__(self):
        return f"{self.booker} - {self.journey}"