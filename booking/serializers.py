from rest_framework import serializers

from booking.models import Booking, Country, EquipmentChoice, EquipmentType, Place, Vehicle

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
        exclude = ['timestamp', 'id']
        read_only_fields = ('session_key', )

    def create(self, validated_data):
        request = self.context.get('request')
        request.session.flush()
        request.session.save()
        session_key = request.session.session_key
        print(session_key)
        equipment_choices_data = validated_data.pop('equipment_choices')

        booking = Booking.objects.create(session_key = session_key, **validated_data)
        equipment_choices = [EquipmentChoice(**eqp_data) for eqp_data in equipment_choices_data]
        choices = EquipmentChoice.objects.bulk_create(equipment_choices)
        for c in choices:
            booking.equipment_choices.add(c)
        booking.save()
        return booking

    def update(self, instance, validated_data):
        instance.equipment_choices.all().delete()
        equipment_choices_data = validated_data.pop('equipment_choices')
        equipment_choices = [EquipmentChoice(**eqp_data) for eqp_data in equipment_choices_data]
        choices = EquipmentChoice.objects.bulk_create(equipment_choices)
        for c in choices:
            instance.equipment_choices.add(c)
        instance.save()
        return super().update(instance=instance, validated_data=validated_data)

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