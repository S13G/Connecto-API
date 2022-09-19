from django.views.decorators.http import require_http_methods
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
# from rest_framework.pagination import PageNumberPagination

from booking.models import Booking, Country, EquipmentType, Place, Vehicle, Payment
from booking.serializers import BookVehicleSerializer
import stripe

class PlaceView(APIView):   
   def get(self, request):
      places = Place.objects.select_related('country')
      data = []
      for p in places:
         data.append({'name': p.name, 'country':p.country.name, 'category':p.category, 'code':p.code, 'longitude':p.longitude, 'latitude':p.latitude}.copy())
      return Response(data, status=200)

class CountryView(APIView):
   def get(self, request):
      countries = Country.objects.values('name', 'code')
      return Response(countries, status=200)

class VehicleView(APIView):
   def get(self, request):
      vehicles = Vehicle.objects.values('vehicle_make_and_model', 'category', 'seats', 'baggage', 'tag', 'current_price', 'old_price')
      return Response(vehicles, status=200)

class EquipmentTypeView(APIView):
   def get(self, request):
      types = EquipmentType.objects.values('name', 'price')
      return Response(types, status=200)

class BookVehicleView(CreateAPIView):
   serializer_class = BookVehicleSerializer
   queryset = Booking.objects.all()

class BookingUpdateView(RetrieveUpdateAPIView):
   serializer_class = BookVehicleSerializer

   def get_object(self, request):
      return Booking.objects.get(session_key=request.session.session_key)

class MakePaymentView(APIView):
   def post(self, request):
      data = request.data
      booking = Booking.objects.filter(session_key = request.session.session_key)
      if booking.exists():
         booking = booking.get()
      else:
         return Response('Booking object not found', status=400)
      
      token = data.get('stripe_token')
      if token:
         payment = Payment.objects.create(booking=booking, session_key=booking.session_key, stripe_token=token)

         try:
            charge = stripe.Charge.create(
                  amount=data.get('amount'),
                  currency='USD',
                  source=token,
                  description='Charge from Connecto',
                  statement_descriptor="22 Characters max",
                  metadata={'order_id': payment.transaction_id},
                  receipt_email=booking.email_address
            )

            # Only confirm an order after you have status: succeeded
            print("______STATUS_____", charge['status'])  # should be succeeded
            if charge['status'] == 'succeeded':
               return Response('Your transaction was successful.', status=200)
            else:
               raise stripe.error.CardError
         except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            print('Status is: %s' % e.http_status)
            print('Type is: %s' % err.get('type'))
            print('Code is: %s' % err.get('code'))
            print('Message is %s' % err.get('message'))
            return Response(err.get('message'), status=400)
         except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            return Response("The API was not able to respond, try again.", status=429)
         except stripe.error.InvalidRequestError as e:
            # invalid parameters were supplied to Stripe's API
            return Response("Invalid parameters, unable to process payment.", status=400)
         except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            return Response("Authentication Failed. Try again", status=401)
         except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            return Response('Network communication failed, try again.', status=400)
         except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe
            # send yourself an email
            return Response('Internal Error, contact support.', status=400)
         # Something else happened, completely unrelated to Stripe
         except Exception as e:
            return Response('Unable to process payment, try again later.', status=500)
      else:
         return Response('Token cannot be null', status=400)
