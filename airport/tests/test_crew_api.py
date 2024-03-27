from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Crew
from airport.serializers.crew_serializers import CrewSerializer
from airport.utils.samples import sample_user, sample_crew, sample_superuser

CREW_URL = reverse("airport:crew-list")


class UnauthenticatedCrewApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(CREW_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_list_crew(self):
        sample_crew()
        sample_crew(position="copilot")

        response = self.client.get(CREW_URL)

        crews = Crew.objects.all()
        serializer = CrewSerializer(crews, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("results"), serializer.data)

    def test_create_crew_forbidden(self):
        payload = {
            "first_name": "Bob",
            "last_name": "Sample",
            "position": "pilot",
        }

        response = self.client.post(CREW_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminCrewApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = sample_superuser()
        self.client.force_authenticate(self.user)

    def test_create_crew(self):
        payload = {
            "first_name": "Bob",
            "last_name": "Sample",
            "position": "pilot",
        }

        response = self.client.post(CREW_URL, payload)
        crew = Crew.objects.get(id=response.data.get("id"))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(crew, key))
