from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Airplane
from airport.serializers.airplane_serializers import AirplaneSerializer
from airport.utils.samples import (
    sample_user,
    sample_superuser,
    sample_airplane,
    sample_airplane_type
)


AIRPLANE_URL = reverse("airport:airplane-list")
AIRPLANE_DETAIL_URL = reverse("airport:airplane-detail", kwargs={"pk": 1})


class UnauthenticatedAirplaneApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(AIRPLANE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneTypeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)
        self.airplane = sample_airplane()

    def test_list_airplane(self):
        sample_airplane(name="super Jet")
        response = self.client.get(AIRPLANE_URL)

        airplane = Airplane.objects.all()
        serializer = AirplaneSerializer(airplane, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("results"), serializer.data)

    def test_retrieve_airplane_detail(self):
        response = self.client.get(AIRPLANE_DETAIL_URL)
        serializer = AirplaneSerializer(self.airplane)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_airplane_forbidden(self):
        payload = {
            "name": "Test Airplane",
            "rows": 2,
            "seats_in_row": 10,
            "airplane_type": sample_airplane_type().id
        }
        response = self.client.post(AIRPLANE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_airplane_forbidden(self):
        payload = {"name": "Test Airplane22"}
        response = self.client.patch(AIRPLANE_DETAIL_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = sample_superuser()
        self.client.force_authenticate(self.user)
        self.airplane = sample_airplane()

    def test_create_airplane(self):
        payload = {
            "name": "Test Airplane",
            "rows": 2,
            "seats_in_row": 10,
            "airplane_type": sample_airplane_type().id
        }
        response = self.client.post(AIRPLANE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_airplane(self):
        payload = {"name": "Test Airplane123"}
        response = self.client.patch(AIRPLANE_DETAIL_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_airplane_not_allowed(self):
        res = self.client.delete(AIRPLANE_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
