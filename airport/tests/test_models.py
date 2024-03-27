from django.core.exceptions import ValidationError
from django.test import TestCase

from airport.utils.samples import (
    sample_crew,
    sample_airplane_type,
    sample_airplane,
    sample_airport,
    sample_route,
    sample_flight,
    sample_order,
    sample_ticket,
    sample_user
)


class CrewModelTest(TestCase):

    def setUp(self) -> None:
        self.crew = sample_crew()

    def test_crew_full_name(self):
        self.assertEqual(
            self.crew.full_name,
            f"{self.crew.first_name} {self.crew.last_name}"
        )

    def test_crew_str(self):
        self.assertEqual(
            str(self.crew),
            f"{self.crew.full_name} - {self.crew.position}"
        )


class AirplaneTypeModelTest(TestCase):

    def setUp(self) -> None:
        self.airplane_type = sample_airplane_type()

    def test_airplane_type_str(self):
        self.assertEqual(str(self.airplane_type), self.airplane_type.name)


class AirplaneModelTest(TestCase):

    def setUp(self) -> None:
        self.airplane = sample_airplane()

    def test_airplane_capacity(self):
        self.assertEqual(
            self.airplane.capacity,
            self.airplane.rows * self.airplane.seats_in_row
        )

    def test_airplane_str(self):
        self.assertEqual(
            str(self.airplane),
            f"Airplane: {self.airplane.name}, "
            f"Type: {self.airplane.airplane_type}"
        )


class AirportModelTest(TestCase):

    def setUp(self) -> None:
        self.airport = sample_airport()

    def test_airport_str(self):
        self.assertEqual(
            str(self.airport),
            f"{self.airport.name} - {self.airport.closest_big_city}"
        )


class RouteModelTest(TestCase):

    def setUp(self) -> None:
        self.route = sample_route()

    def test_route_str(self):
        self.assertEqual(
            str(self.route),
            f"{self.route.source.name}-{self.route.destination.name}"
        )


class FlightModelTest(TestCase):

    def setUp(self) -> None:
        self.flight = sample_flight()
        self.flight.crew.add(sample_crew())

    def test_flight_str(self):
        self.assertEqual(
            str(self.flight),
            f"{self.flight.route} - {self.flight.airplane.name}"
        )


class OrderModelTest(TestCase):

    def setUp(self) -> None:
        self.order = sample_order()

    def test_order_str(self):
        self.assertEqual(
            str(self.order),
            f"Order #{self.order.id}: {self.order.created_at}"
        )


class TicketModelTest(TestCase):

    def setUp(self) -> None:
        self.flight = sample_flight()
        self.ticket = sample_ticket(flight=self.flight)

    def test_validate_unique_together(self):
        order = sample_order(user=sample_user(email="test_user2@test.com"))

        with self.assertRaises(ValidationError):
            sample_ticket(order=order, flight=self.flight)

    def test_validate_ticket(self):
        order = sample_order(user=sample_user(email="test_user2@test.com"))

        with self.assertRaises(ValidationError):
            sample_ticket(row=20, seat=35, order=order, flight=self.flight)
