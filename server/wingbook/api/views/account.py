from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers.account import AccountSerializer
from api.models.account import Account
from api.models.person import Person

class AccountViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing account instances.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name']

    def create(self, request, *args, **kwargs):
        
        if not request.data.get("name") and request.data.get("person"):
            person = request.data["person"]
            person = Person.objects.filter(id=person).values("first_name", "last_name").first()
            if person:
                request.data["name"] = f"{person['first_name']} {person['last_name']}"
            else:
                return Response({"error": "Person not found"}, status=status.HTTP_404_NOT_FOUND)
        if Account.objects.filter(name=request.data["name"]).exists():
            return Response({"error": "Account with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if "person" in request.data and Account.objects.filter(person=request.data["person"]).exists():
            return Response({"error": "Account with this person already exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        account = self.get_object()
        serializer = self.get_serializer(account, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Account updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        account = self.get_object()
        account.delete()
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)