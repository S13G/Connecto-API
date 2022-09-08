from django.core.validators import MinValueValidator
from django.db import models
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


class Journey(models.Model):
    from_place = models.ForeignKey(
        Place, on_delete=models.CASCADE, null=True, related_name="journey_from_place")
    to_place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    current_journey_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True)
    old_journey_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True)
    passengers = models.IntegerField(validators=[MinValueValidator(1)])
    distance = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    session_key = models.CharField(max_length=10000, null=True, editable=False)

    def save(self, *args, **kwargs):
        location1 = (self.from_place.latitude, self.from_place.longitude)
        location2 = (self.to_place.latitude, self.to_place.longitude)
        journey_distance = hs.haversine(location1, location2)
        self.distance = journey_distance
        price_per_km = self.vehicle.current_price
        self.current_journey_price = journey_distance * price_per_km
        self.old_journey_price = journey_distance * self.vehicle.old_price
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
    ROUTE = [
        ('With Return', 'With Return'),
        ('One Way', 'One Way'),
    ]
    reference_ID = ShortUUIDField(
        max_length=5, unique=True, editable=False)
    route = models.CharField(
        max_length=255, choices=ROUTE, default='With Return')
    booker = models.ForeignKey(
        Booker, on_delete=models.CASCADE, related_name="customer", default=None)
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, default=None)
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    departure = models.DateField()
    returning = models.DateField()
    arrival_flight_number = models.CharField(
        max_length=20, null=True, blank=True)
    landing_time = models.TimeField(default=None)
    drop_off = models.CharField(max_length=255, default=None)
    return_date = models.DateField()
    pickup_time = models.TimeField(default=None)
    pickup_address = models.CharField(max_length=255, default=None)
    departure_flight_number = models.CharField(
        max_length=20, null=True, blank=True)
    departure_flight_time = models.TimeField(default=None)
    session_key = models.CharField(max_length=10000, null=True, editable=False)

    def __str__(self):
        return f"{self.airport}"


class EquipmentType(models.Model):
    CHILD_SEAT = 5.00
    INFANT_SEAT = 5.00
    WHEELCHAIR = 0
    BOOSTER_SEAT = 5.00
    EXTRA_STOP_IN_TOWN = 10.00
    SKIS_AND_SNOWBOARD = 5.00
    BICYCLE = 10.00

    EQUIPMENT_CHOICE = [
        (CHILD_SEAT, 'Child Seat'),
        (INFANT_SEAT, 'Infant Seat'),
        (WHEELCHAIR, 'Wheelchair'),
        (BOOSTER_SEAT, 'Booster Seat'),
        (EXTRA_STOP_IN_TOWN, 'Extra Stop in Town'),
        (SKIS_AND_SNOWBOARD, 'Ski and Snowboard'),
        (BICYCLE, 'Bicycle'),
    ]
    name = models.CharField(choices=EQUIPMENT_CHOICE,
                            max_length=255, default=None)
    quantity = models.IntegerField(null=True)
    date_created = models.DateTimeField(null=True)
    session_key = models.CharField(max_length=10000, null=True, editable=False)

    def __str__(self):
        return f"{self.name}"


class Equipment(models.Model):
    equipment = models.ManyToManyField(EquipmentType)
    first_item_count = models.IntegerField(default=None)
    return_item_count = models.IntegerField(default=None)
    booking = models.ForeignKey(
        Booking, default=None, on_delete=models.CASCADE, related_name="extras")
    session_key = models.CharField(max_length=10000, null=True, editable=False)

    def __str__(self):
        return f"{self.equipment}"
