from rest_framework import mixins, viewsets

from airport.models import (
    Crew,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Flight,
    Order,
)
from airport.serializers.airplane_serializers import AirplaneSerializer
from airport.serializers.airplane_type_serializers import (
    AirplaneTypeSerializer
)
from airport.serializers.airport_serializers import AirportSerializer
from airport.serializers.crew_serializers import CrewSerializer
from airport.serializers.flight_serializers import FlightSerializer
from airport.serializers.order_serializers import OrderSerializer
from airport.serializers.route_serializers import RouteSerializer


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirplaneTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class AirportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)