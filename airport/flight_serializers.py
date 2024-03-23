from rest_framework import serializers

from airport.models import Flight


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
