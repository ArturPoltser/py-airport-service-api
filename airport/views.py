from rest_framework import mixins, viewsets

from airport.models import Crew
from airport.serializers.crew_serializers import CrewSerializer


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
