from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Order
from airport.serializers.order_serializers import OrderListSerializer
from airport.utils.samples import sample_user, sample_order, sample_flight

ORDER_URL = reverse("airport:order-list")


class UnauthenticatedOrderApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(ORDER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedOrderApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_list_order(self):
        sample_order(user=self.user)
        sample_order(user=self.user)

        response = self.client.get(ORDER_URL)

        orders = Order.objects.filter(user=self.user)
        serializer = OrderListSerializer(orders, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("results"), serializer.data)

    def test_create_order_with_ticket(self):
        ticket_data = {
            "row": 1,
            "seat": 1,
            "flight": sample_flight().id
        }
        data = {
            "tickets": [ticket_data]
        }

        response = self.client.post(ORDER_URL, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_without_ticket(self):
        payload = {"tickets": []}

        response = self.client.post(ORDER_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("tickets").get("non_field_errors")[0],
            "This list may not be empty."
        )
