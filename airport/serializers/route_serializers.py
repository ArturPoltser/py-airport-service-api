from rest_framework import serializers

from airport.models import Route


class RouteSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs.get("source") == attrs.get("destination"):
            raise serializers.ValidationError(
                "Source can't be same as Destination"
            )
        return attrs

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")
