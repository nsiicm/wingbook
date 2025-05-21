from rest_framework import serializers
from api.models.flight import Flight
from api.models.plane import Plane
from api.models.person import Person

class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = ['id', 'model', 'registration_number']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class FlightSerializerDetail(serializers.ModelSerializer):
    plane = PlaneSerializer()
    pilot_in_command = PersonSerializer()
    passengers = PersonSerializer(many=True)

    class Meta:
        model = Flight
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'
