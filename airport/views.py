from rest_framework import mixins, viewsets

from airport.models import Crew, AirplaneType
from airport.serializers.crew_serializers import CrewSerializer
from airport.serializers.airplane_type_serializers import (
    AirplaneTypeSerializer
)


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
