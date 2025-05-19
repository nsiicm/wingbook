from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.plane import PlaneViewSet
from api.views.person import PersonViewSet
from api.views.flight import FlightViewSet

router = DefaultRouter()
router.register(r'planes', PlaneViewSet)
router.register(r'people', PersonViewSet)
router.register(r'flights', FlightViewSet)

urlpatterns = [
    path('', include(router.urls)),
]