from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers.operation import OperationSerializer, OperationSerializerDetail
from api.models.operation import Operation
from api.models.transaction import Transaction

class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'id': ["exact"],
    }
    def destroy(self, request, *args, **kwargs):
        operation = self.get_object()
        operation.delete()
        return Response({"message": "Operation deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        operation = self.get_object()
        serializer = self.get_serializer(operation, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Operation updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        #if request.data.get('type') == 'transfer':
        #    # Create a transfer operation
        #    source_account = serializer.validated_data.get('source_account')
        #    destination_account = serializer.validated_data.get('destination_account')
        #    amount = serializer.validated_data.get('amount')
        #    # Perform the transfer logic here
        #    # For example, you might want to update the balances of the accounts involved
        #    source_transaction = Transaction.objects.create(
        #        account=source_account,
        #        amount=-amount,
        #        operation=serializer.instance
        #    )
        #    source_transaction.save()
        #    destination_transaction = Transaction.objects.create(
        #        account=destination_account,
        #        amount=amount,
        #        operation=serializer.instance
        #    )
        #    destination_transaction.save()
        #if request.data.get('type') == 'credit':
        #    # Create a credit operation
        #    account = serializer.validated_data.get('destination_account')
        #    amount = serializer.validated_data.get('amount')
        #    # Perform the credit logic here
        #    # For example, you might want to update the balance of the account
        #    transaction = Transaction.objects.create(
        #        account=account,
        #        amount=amount,
        #        operation=serializer.instance
        #    )
        #    transaction.save()
        #if request.data.get('type') == 'debit':
        #    # Create a debit operation
        #    account = serializer.validated_data.get('destination_account')
        #    amount = serializer.validated_data.get('amount')
        #    # Perform the debit logic here
        #    # For example, you might want to update the balance of the account
        #    transaction = Transaction.objects.create(
        #        account=account,
        #        amount=-amount,
        #        operation=serializer.instance
        #    )
        #    transaction.save()
        #if request.data.get('type') == 'refund':
        #    # Create a refund operation
        #    source_account = serializer.validated_data.get('source_account')
        #    destination_account = serializer.validated_data.get('destination_account')
        #    amount = serializer.validated_data.get('amount')
        #    # Perform the refund logic here
        #    # For example, you might want to update the balances of the accounts involved
        #    source_transaction = Transaction.objects.create(
        #        account=source_account,
        #        amount=amount,
        #        operation=serializer.instance
        #    )
        #    source_transaction.save()
        #    destination_transaction = Transaction.objects.create(
        #        account=destination_account,
        #        amount=amount,
        #        operation=serializer.instance
        #    )
        #    destination_transaction.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = OperationSerializerDetail(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
