from rest_framework import serializers
import django_filters
from api.models.account import Account
from api.models.transaction import Transaction

class AccountSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    class Meta:
        model = Account
        fields = '__all__'

    def get_balance(self, obj):
        # Example: compute balance from related transactions
        return obj.get_balance()  # or however you compute it
