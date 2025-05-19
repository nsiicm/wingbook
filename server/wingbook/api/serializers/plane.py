from rest_framework import serializers
from api.models.plane import Plane

class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = '__all__'