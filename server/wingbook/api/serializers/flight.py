from rest_framework import serializers
from api.models.flight import Flight
from api.models.plane import Plane
from api.models.person import Person

class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = ['model', 'registration_number']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['last_name', 'first_name']

class FlightSerializer(serializers.ModelSerializer):
    plane = PlaneSerializer()
    pilot_in_command = PersonSerializer()
    class Meta:
        model = Flight
        fields = '__all__'
