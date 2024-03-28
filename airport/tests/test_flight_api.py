import datetime
from operator import itemgetter

from django.db.models import F, Count
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Flight
from airport.serializers.flight_serializers import (
    FlightListSerializer,
    FlightDetailSerializer
)
from airport.utils.samples import (
    sample_user,
    sample_superuser,
    sample_flight,
    sample_airport, sample_route, sample_airplane, sample_crew
)

FLIGHT_URL = reverse("airport:flight-list")


def detail_url(flight_id):
    return reverse("airport:flight-detail", args=[flight_id])


class UnauthenticatedFlightApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(FLIGHT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightTypeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)
        self.flight = sample_flight()
        self.other_flight = sample_flight(
            route=sample_route(
                source=sample_airport(
                    closest_big_city="Test_City"
                ),
                destination=sample_airport(
                    closest_big_city="Other_City"
                )
            ),
            departure_time=datetime.datetime(2024, 5, 5, 14, 45),
            arrival_time=datetime.datetime(2024, 5, 7, 14, 45)
        )
        self.flights = Flight.objects.annotate(
            tickets_available=(
                F("airplane__rows") * F("airplane__seats_in_row")
                - Count("tickets")
            )
        )

    def test_list_flight(self):
        response = self.client.get(FLIGHT_URL)
        serializer = FlightListSerializer(self.flights, many=True)
        serializer_data = sorted(serializer.data, key=itemgetter("id"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("results"), serializer_data)

    def test_filter_flights_by_from_city(self):
        response = self.client.get(FLIGHT_URL, {"from": "te"})

        serializer1 = FlightListSerializer(
            self.flights.get(id=self.flight.id)
        )
        serializer2 = FlightListSerializer(
            self.flights.get(id=self.other_flight.id)
        )

        self.assertNotIn(serializer1.data, response.data.get("results"))
        self.assertIn(serializer2.data, response.data.get("results"))

    def test_filter_flights_by_to_city(self):
        response = self.client.get(FLIGHT_URL, {"to": "ot"})

        serializer1 = FlightListSerializer(
            self.flights.get(id=self.flight.id)
        )
        serializer2 = FlightListSerializer(
            self.flights.get(id=self.other_flight.id)
        )

        self.assertNotIn(serializer1.data, response.data.get("results"))
        self.assertIn(serializer2.data, response.data.get("results"))

    def test_filter_flights_by_departure_date(self):
        response = self.client.get(FLIGHT_URL, {"departure_date": "2024-4-4"})

        serializer1 = FlightListSerializer(
            self.flights.get(id=self.flight.id)
        )
        serializer2 = FlightListSerializer(
            self.flights.get(id=self.other_flight.id)
        )

        self.assertIn(serializer1.data, response.data.get("results"))
        self.assertNotIn(serializer2.data, response.data.get("results"))

    def test_filter_flights_by_arrival_date(self):
        response = self.client.get(FLIGHT_URL, {"arrival_date": "2024-5-7"})

        serializer1 = FlightListSerializer(
            self.flights.get(id=self.flight.id)
        )
        serializer2 = FlightListSerializer(
            self.flights.get(id=self.other_flight.id)
        )

        self.assertNotIn(serializer1.data, response.data.get("results"))
        self.assertIn(serializer2.data, response.data.get("results"))

    def test_retrieve_flight_detail(self):
        response = self.client.get(detail_url(self.flight.id))
        serializer = FlightDetailSerializer(self.flight)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_flight_forbidden(self):
        response = self.client.post(FLIGHT_URL, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_flight_forbidden(self):
        payload = {
            "departure_time": datetime.datetime(2024, 4, 4, 14, 45),
        }
        res = self.client.patch(detail_url(self.flight.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_flight_forbidden(self):
        res = self.client.delete(detail_url(self.flight.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminFlightApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = sample_superuser()
        self.client.force_authenticate(self.user)
        self.flight = sample_flight()

    def test_create_flight(self):
        payload = {
            "route": sample_route().id,
            "airplane": sample_airplane().id,
            "departure_time": datetime.datetime(2024, 4, 4, 14, 45),
            "arrival_time": datetime.datetime(2024, 4, 5, 14, 45),
            "crew": [sample_crew().id]
        }
        response = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_flight_with_invalid_data(self):
        payload = {
            "route": sample_route().id,
            "airplane": sample_airplane().id,
            "departure_time": datetime.datetime(2024, 4, 4, 14, 45),
            "arrival_time": datetime.datetime(2024, 4, 3, 14, 45),
            "crew": [sample_crew().id]
        }
        response = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("non_field_errors")[0],
            "Arrival time can't be lesser than departure time"
        )

    def test_update_flight(self):
        payload = {
            "departure_time": datetime.datetime(2024, 4, 4, 14, 50),
            "arrival_time": datetime.datetime(2024, 4, 5, 14, 55)
        }

        response = self.client.patch(detail_url(self.flight.id), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_flight(self):
        response = self.client.delete(detail_url(self.flight.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
