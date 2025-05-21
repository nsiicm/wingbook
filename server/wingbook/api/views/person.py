from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers.person import PersonSerializer
from api.models.person import Person
from api.models.account import Account

class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows persons to be viewed or edited.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'id': ["exact"],
        'first_name': ["exact", "icontains"],
        'last_name': ["exact", "icontains"],
        'is_pilot': ["exact"],
        'is_instructor': ["exact"],
        'is_main_pilot': ["exact"],
    }  # Add any other fields you want to filter by

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validator(serializer)
        self.perform_create(serializer)
        # Automatically create an account
        account = Account.objects.create(
            name=f"{serializer.validated_data['first_name']} {serializer.validated_data['last_name']}",
            person=serializer.instance
        )
        account.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        person = self.get_object()
        person.delete()
        return Response({"message": "Person deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        person = self.get_object()
        serializer = self.get_serializer(person, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.validator(serializer)
        self.perform_update(serializer)
        return Response({"message": "Person updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def validator(self, serializer):
        # Check If instructor or main pilot is pilot
        if (serializer.validated_data.get('is_instructor') or serializer.validated_data.get('is_main_pilot')) and not serializer.validated_data.get('is_pilot'):
            return Response({"error": "If instructor or main pilot is true, pilot must also be true."}, status=status.HTTP_400_BAD_REQUEST)