from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from airport.models import Ticket
from airport.serializers.flight_serializers import FlightOrderSerializer


class TicketSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs.get("row"),
            attrs.get("seat"),
            attrs.get("flight").airplane,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(),
                fields=("row", "seat", "flight")
            )
        ]


class TicketListSerializer(TicketSerializer):
    flight = FlightOrderSerializer(many=False, read_only=True)
