from rest_framework import serializers

from airport.models import Flight, Ticket
from airport.serializers.airplane_serializers import AirplaneDetailSerializer
from airport.serializers.crew_serializers import CrewDetailSerializer
from airport.serializers.route_serializers import RouteDetailSerializer


class FlightSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs.get("departure_time") >= attrs.get("arrival_time"):
            raise serializers.ValidationError(
                "Arrival time can't be lesser than departure time"
            )
        return attrs

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew"
        )


class FlightListSerializer(FlightSerializer):
    route = serializers.StringRelatedField(read_only=True)
    airplane_name = serializers.CharField(
        source="airplane.name", read_only=True
    )
    airplane_capacity = serializers.IntegerField(
        source="airplane.capacity", read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "departure_time",
            "arrival_time",
            "airplane_name",
            "airplane_capacity",
            "tickets_available"
        )


class FlightTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("row", "seat")


class FlightDetailSerializer(FlightSerializer):
    route = RouteDetailSerializer(read_only=True)
    airplane = AirplaneDetailSerializer(read_only=True)
    crew = CrewDetailSerializer(many=True, read_only=True)
    taken_tickets = FlightTicketSerializer(
        source="tickets",
        many=True,
        read_only=True
    )

    class Meta(FlightSerializer.Meta):
        fields = FlightSerializer.Meta.fields + ("taken_tickets", )


class FlightOrderSerializer(serializers.ModelSerializer):
    route = serializers.StringRelatedField(read_only=True)
    airplane_name = serializers.CharField(
        source="airplane.name", read_only=True
    )

    class Meta:
        model = Flight
        fields = (
            "route",
            "departure_time",
            "arrival_time",
            "airplane_name"
        )
