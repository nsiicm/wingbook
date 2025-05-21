from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.plane import PlaneViewSet
from api.views.person import PersonViewSet
from api.views.flight import FlightViewSet
from api.views.account import AccountViewSet
from api.views.transaction import TransactionViewSet
from api.views.operation import OperationViewSet

router = DefaultRouter()
router.register(r'planes', PlaneViewSet)
router.register(r'people', PersonViewSet)
router.register(r'flights', FlightViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'operations', OperationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]