from rest_framework import serializers

from airport.models import Airplane


class AirplaneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "airplane_type",
        )


class AirplaneDetailSerializer(AirplaneSerializer):
    airplane_type = serializers.SlugRelatedField(
        slug_field="name", read_only=True
    )
