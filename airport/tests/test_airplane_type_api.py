from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import AirplaneType
from airport.serializers.airplane_type_serializers import (
    AirplaneTypeSerializer
)
from airport.utils.samples import (
    sample_user,
    sample_superuser,
    sample_airplane_type
)


AIRPLANE_TYPE_URL = reverse("airport:airplanetype-list")


class UnauthenticatedAirplaneTypeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(AIRPLANE_TYPE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneTypeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_list_airplane_type(self):
        sample_airplane_type()
        sample_airplane_type(name="super Jet")

        response = self.client.get(AIRPLANE_TYPE_URL)

        airplane_type = AirplaneType.objects.all()
        serializer = AirplaneTypeSerializer(airplane_type, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("results"), serializer.data)

    def test_create_airplane_type_forbidden(self):
        payload = {
            "name": "Test Type",
        }

        response = self.client.post(AIRPLANE_TYPE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneTypeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = sample_superuser()
        self.client.force_authenticate(self.user)

    def test_create_airplane_type(self):
        payload = {"name": "Test Airplane Type"}

        response = self.client.post(AIRPLANE_TYPE_URL, payload)
        airplane_type = AirplaneType.objects.get(id=response.data.get("id"))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(airplane_type.name, getattr(airplane_type, "name"))
