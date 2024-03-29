from datetime import datetime

from django.db.models import F, Count
from drf_spectacular.utils import extend_schema_view
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from airport.models import (
    Crew,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Flight,
    Order,
)
from airport.paginations import OrderPagination
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.serializers.airplane_serializers import AirplaneSerializer
from airport.serializers.airplane_type_serializers import (
    AirplaneTypeSerializer
)
from airport.serializers.airport_serializers import AirportSerializer
from airport.serializers.crew_serializers import CrewSerializer
from airport.serializers.flight_serializers import (
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer
)
from airport.serializers.order_serializers import (
    OrderSerializer,
    OrderListSerializer,
)
from airport.serializers.route_serializers import (
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer
)
from airport.utils.schemas import flight_list_schema, route_list_schema


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


@extend_schema_view(
    list=route_list_schema()
)
class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            if source := self.request.query_params.get("source"):
                queryset = queryset.filter(source__name__icontains=source)

            if destination := self.request.query_params.get("destination"):
                queryset = queryset.filter(
                    destination__name__icontains=destination
                )

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return RouteSerializer


@extend_schema_view(
    list=flight_list_schema()
)
class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list":
            current_time = datetime.now()

            queryset = (
                queryset
                .select_related(
                    "route__source",
                    "route__destination",
                    "airplane"
                )
                .filter(departure_time__gt=current_time)
                .annotate(
                    tickets_available=(
                        F("airplane__rows") * F("airplane__seats_in_row")
                        - Count("tickets")
                    )
                )
            )

            if from_city := self.request.query_params.get("from"):
                queryset = queryset.filter(
                    route__source__closest_big_city__icontains=from_city
                )

            if to_city := self.request.query_params.get("to"):
                queryset = queryset.filter(
                    route__destination__closest_big_city__icontains=to_city
                )

            if departure := self.request.query_params.get("departure_date"):
                departure_date = datetime.strptime(departure, "%Y-%m-%d")
                queryset = queryset.filter(
                    departure_time__date=departure_date
                )

            if arrival := self.request.query_params.get("arrival_date"):
                arrival_date = datetime.strptime(arrival, "%Y-%m-%d")
                queryset = queryset.filter(arrival_time__date=arrival_date)

        if self.action == "retrieve":
            queryset = (
                queryset
                .select_related(
                    "airplane__airplane_type",
                    "route__source",
                    "route__destination"
                )
                .prefetch_related("crew")
            )

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightSerializer


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route__source",
        "tickets__flight__route__destination",
        "tickets__flight__airplane"
    )
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
