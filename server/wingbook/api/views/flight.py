from decimal import Decimal
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
import logging

logger = logging.getLogger("django")

from api.serializers.flight import FlightSerializer, FlightSerializerDetail
from api.models.flight import Flight
from api.models.operation import Operation
from api.models.person import Person
from api.models.account import Account

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
        self.manage_operations(serializer)
        return Response({"message": "Flight updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        request.data['landing_day_num'] = request.data.get('landing_day_num', 0)
        if not isinstance(request.data['landing_day_num'], (int, float)):
            request.data['landing_day_num'] = 0
        request.data['landing_night_num'] = request.data.get('landing_night_num', 0)
        if not isinstance(request.data['landing_night_num'], (int, float)):
            request.data['landing_night_num'] = 0
        request.data['ifr_apch_num'] = request.data.get('ifr_apch_num', 0)
        if not isinstance(request.data['ifr_apch_num'], (int, float)):
            request.data['ifr_apch_num'] = 0
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Create operations from flight
        self.manage_operations(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def manage_operations(self, serializer):
        operations = Operation.objects.filter(flight=serializer.instance.id)
        if operations.exists():
            for operation in operations:
                operation.delete()
        pob = len(serializer.validated_data.get('passengers'))
        if pob > 0:
            cost = serializer.validated_data['price']
            num_done = 0
            total_perc = 0
            passengers_cost = {}
            passengers_perc = serializer.validated_data.get('passengers_perc')
            for passenger_id, value in passengers_perc.items():
                passenger_id = int(passenger_id)
                value = value / 100
                passengers_cost[passenger_id] = cost * (Decimal(str(value)))
                total_perc += value
                num_done += 1
            remaining_perc = 1 - total_perc
            perc_remaining_person = remaining_perc / ((pob + 1)- num_done)
            for passenger in serializer.validated_data.get('passengers'):
                if passenger.id not in passengers_cost:
                    passengers_cost[passenger.id] = cost * (Decimal(str(perc_remaining_person)))
            logger.info(f"Passengers cost: {passengers_cost}")
            for passenger in serializer.validated_data.get('passengers'):
                passenger = Person.objects.get(id=passenger.id)
                passenger_account = Account.objects.get(person=passenger.id)
                Operation.objects.create(
                    type="debit",
                    date=serializer.validated_data['date'],
                    amount=passengers_cost[passenger.id],
                    description=f"Flight {serializer.instance.id}",
                    destination_account=passenger_account,
                    flight=serializer.instance,
                )
        plane_account = Account.objects.get(plane=serializer.validated_data['plane'].id)
        Operation.objects.create(
            type="debit",
            date=serializer.validated_data['date'],
            amount=serializer.validated_data['price'],
            description=f"Flight {serializer.instance.id}",
            destination_account=plane_account,
            flight=serializer.instance,
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = FlightSerializerDetail(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = FlightSerializerDetail(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)