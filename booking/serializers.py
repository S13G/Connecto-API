from wsgiref import validate
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

    def create(self, validated_data):
        equipment_choices_data = validated_data.pop('equipment_choices')
        booking = Booking.objects.create(**validated_data)
        equipment_choices = [EquipmentChoice(**eqp_data) for eqp_data in equipment_choices_data]
        choices = EquipmentChoice.objects.bulk_create(equipment_choices)
        for c in choices:
            booking.equipment_choices.add(c)
        booking.save()
        return booking
