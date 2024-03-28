from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Route
from airport.serializers.route_serializers import (
    RouteListSerializer,
    RouteDetailSerializer
)
from airport.utils.samples import (
    sample_user,
    sample_superuser,
    sample_route,
    sample_airport
)

ROUTE_URL = reverse("airport:route-list")


def detail_url(route_id):
    return reverse("airport:route-detail", args=[route_id])


class UnauthenticatedRouteApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(ROUTE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteTypeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)
        self.route = sample_route()
        self.other_route = sample_route(
            source=sample_airport(name="Monaco"),
            destination=sample_airport(name="Prague")
        )

    def test_list_route(self):
        sample_route()
        response = self.client.get(ROUTE_URL)

        routes = Route.objects.all()
        serializer = RouteListSerializer(routes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("results"), serializer.data)

    def test_filter_routes_by_source(self):
        res = self.client.get(ROUTE_URL, {"source": "mona"})

        serializer1 = RouteListSerializer(self.route)
        serializer2 = RouteListSerializer(self.other_route)

        self.assertNotIn(serializer1.data, res.data.get("results"))
        self.assertIn(serializer2.data, res.data.get("results"))

    def test_filter_routes_by_destination(self):
        res = self.client.get(ROUTE_URL, {"destination": "prague"})

        serializer1 = RouteListSerializer(self.route)
        serializer2 = RouteListSerializer(self.other_route)

        self.assertNotIn(serializer1.data, res.data.get("results"))
        self.assertIn(serializer2.data, res.data.get("results"))

    def test_retrieve_route_detail(self):
        response = self.client.get(detail_url(self.route.id))
        serializer = RouteDetailSerializer(self.route)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_route_forbidden(self):
        payload = {
            "source": "Test Source",
            "destination": "Test destination",
            "distance": 400,
        }
        response = self.client.post(ROUTE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminRouteApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = sample_superuser()
        self.client.force_authenticate(self.user)
        self.route = sample_route()

    def test_create_route(self):
        payload = {
            "source": sample_airport().id,
            "destination": sample_airport().id,
            "distance": 400,
        }
        response = self.client.post(ROUTE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_route_with_invalid_data(self):
        airport = sample_airport()
        payload = {
            "source": airport.id,
            "destination": airport.id,
            "distance": 400,
        }
        response = self.client.post(ROUTE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("non_field_errors")[0],
            "Source can't be same as Destination"
        )

    def test_update_route_not_allowed(self):
        data = {"distance": 20}

        res = self.client.put(detail_url(self.route.id), data)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_route_not_allowed(self):
        res = self.client.delete(detail_url(self.route.id))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
