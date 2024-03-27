from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Airport
from airport.serializers.airport_serializers import AirportSerializer
from airport.utils.samples import (
    sample_user,
    sample_superuser,
    sample_airport
)

AIRPORT_URL = reverse("airport:airport-list")
AIRPORT_DETAIL_URL = reverse("airport:airport-detail", kwargs={"pk": 1})


class UnauthenticatedAirportApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(AIRPORT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportTypeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)
        self.airport = sample_airport()

    def test_list_airport(self):
        sample_airport(name="Test Air")
        response = self.client.get(AIRPORT_URL)

        airport = Airport.objects.all()
        serializer = AirportSerializer(airport, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("results"), serializer.data)

    def test_retrieve_airport_detail(self):
        response = self.client.get(AIRPORT_DETAIL_URL)
        serializer = AirportSerializer(self.airport)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_airport_forbidden(self):
        payload = {
            "name": "test_airport",
            "closest_big_city": "San Francisco",
        }
        response = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = sample_superuser()
        self.client.force_authenticate(self.user)
        self.airport = sample_airport()

    def test_create_airport(self):
        payload = {
            "name": "Test airport",
            "closest_big_city": "San Francisco",
        }
        response = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_airport_not_allowed(self):
        data = {"closest_big_city": "Test"}

        res = self.client.put(AIRPORT_DETAIL_URL, data)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_airport_not_allowed(self):
        res = self.client.delete(AIRPORT_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
