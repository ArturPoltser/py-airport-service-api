from rest_framework import serializers

from airport.models import Crew


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "position")


class CrewDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "full_name", "position")
