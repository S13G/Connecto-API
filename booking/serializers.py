from rest_framework import serializers
from booking.models import Booking, Country, EquipmentChoice, EquipmentType, Place, Vehicle
from django.conf import settings
from booking.emails import Util
from . tasks import transport_reminder
from datetime import datetime, timedelta, timezone

import stripe

class EquipmentChoiceSerializer(serializers.ModelSerializer):
    equipment = serializers.SlugRelatedField(slug_field='name', queryset=EquipmentType.objects.all(), error_messages={'does_not_exist': 'Invalid Equipment!'})
    class Meta:
        model = EquipmentChoice
        fields = ['quantity', 'equipment']

class BookVehicleSerializer(serializers.ModelSerializer):
    from_place = serializers.SlugRelatedField(slug_field='name', queryset=Place.objects.all(), error_messages={'does_not_exist': 'Place does not exist!'})
    to_place = serializers.SlugRelatedField(slug_field='name', queryset=Place.objects.all(), error_messages={'does_not_exist': 'Place does not exist!'})
    vehicle = serializers.SlugRelatedField(slug_field='vehicle_make_and_model', queryset=Vehicle.objects.all(), error_messages={'does_not_exist': 'Invalid Vehicle!'})
    country = serializers.SlugRelatedField(slug_field='name', queryset=Country.objects.all(), error_messages={'does_not_exist': 'Country does not exist!'})
    equipment_choices = EquipmentChoiceSerializer(many=True)

    class Meta:
        model = Booking
        exclude = ['date_filled', 'id', 'verified']
        read_only_fields = ('transaction_id', )

    def get_fields(self, *args, **kwargs):
        fields = super(BookVehicleSerializer, self).get_fields(*args, **kwargs)
        for f in fields.values():
            f.required = True
        return fields

    def create(self, validated_data):
        if None in validated_data.values():
            raise serializers.ValidationError('Fields are not properly filled')

        equipment_choices_data = validated_data.pop('equipment_choices')
        token = validated_data.pop('stripe_token', None)
        booking = Booking.objects.create(**validated_data)
        equipment_choices = [EquipmentChoice(**eqp_data) for eqp_data in equipment_choices_data]
        choices = EquipmentChoice.objects.bulk_create(equipment_choices)
        for c in choices:
            booking.equipment_choices.add(c)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            
            charge = stripe.Charge.create(
                amount=booking.total_current_price,
                currency='USD',
                source=token,
                description='Charge from Connecto',
                statement_descriptor="22 Characters max",
                metadata={'transaction_id': booking.transaction_id},
                receipt_email=booking.email_address
            )

            # Only confirm an order after you have status: succeeded
            if charge['status'] == 'succeeded':
                booking.verified = True
                booking.save()
                Util.success_booking_email(booking)
                if (booking.departure - datetime.now(timezone.utc)).total_seconds() >= 634800:
                    transport_reminder(booking.id, schedule=booking.departure - timedelta(days=7))
                return booking
            else:
                raise stripe.error.CardError
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            err = serializers.ValidationError(f"{err.get('message')}")
            err.status_code = 400
            raise err
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            err = serializers.ValidationError("The API was not able to respond, try again.")
            err.status_code = 429
            raise err
        except stripe.error.InvalidRequestError as e:
            # invalid parameters were supplied to Stripe's API
            err = serializers.ValidationError("Invalid parameters, unable to process payment.")
            err.status_code = 400
            raise err
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            err = serializers.ValidationError("Authentication Failed. Try again")
            err.status_code = 403
            raise err
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            err = serializers.ValidationError('Network communication failed, try again.')
            err.status_code = 502
            raise err
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe
            # send yourself an email
            err = serializers.ValidationError('Internal Error, contact support.')
            err.status_code = 500
            raise err
        # Something else happened, completely unrelated to Stripe
        except Exception as e:
            err = serializers.ValidationError('Unable to process payment, try again later.')
            err.status_code = 500
            raise err

# {
#   "from_place": "Aalborg Airport",
#   "to_place": "A Coruña Airport",
#   "vehicle": "Audi A8",
#   "country": "Germany",
#   "equipment_choices": [
#     {
#       "quantity": 4,
#       "equipment": "CHILD SEAT"
#     },
#     {
#       "quantity": 3,
#       "equipment": "INFANT SEAT"
#     }
#   ],
#   "route": "With Return",
#   "pronoun": "Mr",
#   "first_name": "John",
#   "last_name": "Doe",
#   "email_address": "Doe@gmail.com",
#   "phone_number": "5434543423",
#   "passengers": 4,
#   "stripe_token": "okdsjisdoihsfdfhisih",
#   "departure": "2022-09-10",
#   "returning": "2022-10-10",
#   "arrival_flight_number": "3243",
#   "landing_time": "09:38:00",
#   "drop_off": "dd",
#   "return_date": "2022-10-10",
#   "pickup_time": "02:43:00",
#   "pickup_address": "ddd",
#   "departure_flight_number": "232323",
#   "departure_flight_time": "09:13:00"
# }