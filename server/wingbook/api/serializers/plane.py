from rest_framework import serializers
from api.models.plane import Plane
from api.serializers.account import AccountSerializer

class PlaneSerializerDetail(serializers.ModelSerializer):
    account = AccountSerializer()
    class Meta:
        model = Plane
        fields = '__all__'

class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = '__all__'