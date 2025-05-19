from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers.flight import FlightSerializer
from api.models.flight import Flight

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'id': ["exact"],
        'departure_airport': ["exact", "icontains"],
        'arrival_airport': ["exact", "icontains"]
    }

    def destroy(self, request, *args, **kwargs):
        flight = self.get_object()
        flight.delete()
        return Response({"message": "Flight deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        flight = self.get_object()
        serializer = self.get_serializer(flight, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Flight updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)