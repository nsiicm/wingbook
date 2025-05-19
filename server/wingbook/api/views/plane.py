from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers.plane import PlaneSerializer
from api.models.plane import Plane


class PlaneViewSet(viewsets.ModelViewSet):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'id': ["exact"],
        'model': ["exact", "icontains"]
    }

    def destroy(self, request, *args, **kwargs):
        plane = self.get_object()
        plane.delete()
        return Response({"message": "Plane deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # Check if it's a partial update (PATCH)
        plane = self.get_object()
        serializer = self.get_serializer(plane, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Plane updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
