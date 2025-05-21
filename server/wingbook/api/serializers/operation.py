from rest_framework import serializers
from api.models.operation import Operation

from api.serializers.account import AccountSerializer

class OperationSerializerDetail(serializers.ModelSerializer):
    source_account = AccountSerializer()
    destination_account = AccountSerializer()

    class Meta:
        model = Operation
        fields = '__all__'

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'