from cloudinary.models import CloudinaryField
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

# from booking.image import get_media_paths

import haversine as hs
import uuid


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
    name = models.CharField(max_length=255, unique=True)
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

    vehicle_make_and_model = models.CharField(max_length=255, unique=True)
    image = CloudinaryField('image', null=True)
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
    name = models.CharField(max_length=255, choices=EQUIPMENT_CHOICE, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)], null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name}"


class EquipmentChoice(models.Model):
    equipment = models.ForeignKey(EquipmentType, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(validators=[MaxValueValidator(5)])
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.equipment}"

    @property
    def total_price(self):
       return self.equipment.price * self.quantity


class Booking(models.Model):
    ROUTE = (
        ('With Return', 'With Return'),
        ('One Way', 'One Way'),
    )
    PRONOUN = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs')
    ]
    route = models.CharField(
        max_length=255, choices=ROUTE, default='With Return')
    
    # booker details
    pronoun = models.CharField(max_length=3, choices=PRONOUN, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email_address = models.EmailField(max_length=254, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    #---------------------------------------------
    
    # journey details
    from_place = models.ForeignKey(
        Place, on_delete=models.CASCADE, null=True, related_name="journey_from_place")
    to_place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    passengers = models.IntegerField(default="1", validators=[MinValueValidator(1)], null=True)
    #--------------------------------------
    
    # equipment choice
    equipment_choices = models.ManyToManyField(EquipmentChoice)
    #-------------------------------------

    # other details
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

    date_filled = models.DateTimeField(default=timezone.now)

    # Payment Details
    transaction_id = models.CharField(max_length=200, null=True, unique=True)
    stripe_token = models.CharField(max_length=255, null=True, unique=True)
    verified = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} = {self.from_place} to {self.to_place}"

    @property
    def journey_distance(self):
        location1 = (Decimal(self.from_place.latitude), Decimal(self.from_place.longitude))
        location2 = (Decimal(self.to_place.latitude), Decimal(self.to_place.longitude))
        return round(Decimal(hs.haversine(location1, location2)), 2)

    @property
    def total_current_price(self):
        equipment_sum = sum([equipment.total_price for equipment in self.equipment_choices.all()])
        price_per_km = self.vehicle.current_price * self.passengers
        total_price = self.journey_distance * (price_per_km / 1000) + equipment_sum
        if self.route == "With Return":
            total_price = total_price * 2 
        return round(total_price, 2)

    @property
    def total_old_price(self):
        equipment_sum = sum([equipment.total_price for equipment in self.equipment_choices.all()])
        old_price_per_km = self.vehicle.old_price * self.passengers
        total_price = self.journey_distance * (old_price_per_km / 1000) + equipment_sum
        if self.route == "With Return":
            total_price = total_price * 2 
        return round(total_price, 2)

    def save(self, *args, **kwargs) -> None:
        while not self.transaction_id:
            unique_code = str(uuid.uuid4()).replace("-", "")[:100]
            transaction_id = str(unique_code)
            similar_obj_trans_id = Booking.objects.filter(transaction_id=transaction_id)
            if not similar_obj_trans_id:
                self.transaction_id = transaction_id                
        super().save(*args, **kwargs)