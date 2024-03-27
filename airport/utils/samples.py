import datetime

from django.contrib.auth import get_user_model

from airport.models import (
    Crew,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Flight,
    Order,
    Ticket
)


def sample_superuser(**params):
    defaults = {
        "email": "admin@admin.com",
        "password": "1qazcde3",
        "first_name": "admin",
        "last_name": "User"
    }
    defaults.update(params)

    return get_user_model().objects.create_superuser(**defaults)


def sample_user(**params):
    defaults = {
        "email": "test_user@test.com",
        "password": "test1234",
        "first_name": "Test",
        "last_name": "User"
    }
    defaults.update(params)

    return get_user_model().objects.create_user(**defaults)


def sample_crew(**params):
    defaults = {
        "first_name": "John",
        "last_name": "Smith",
        "position": "pilot"
    }
    defaults.update(params)

    return Crew.objects.create(**defaults)


def sample_airplane_type(**params):
    defaults = {
        "name": "test_type"
    }
    defaults.update(params)

    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params):
    airplane_type = sample_airplane_type()

    defaults = {
        "name": "airplane_name",
        "rows": 2,
        "seats_in_row": 10,
        "airplane_type": airplane_type
    }
    defaults.update(params)

    return Airplane.objects.create(**defaults)


def sample_airport(**params):
    defaults = {
        "name": "test_airport",
        "closest_big_city": "San Francisco",
    }
    defaults.update(params)

    return Airport.objects.create(**defaults)


def sample_route(**params):
    source = sample_airport()
    destination = sample_airport(
        name="test_airport2", closest_big_city="Sun Diego"
    )

    defaults = {
        "source": source,
        "destination": destination,
        "distance": 600
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


def sample_flight(**params):
    route = sample_route()
    airplane = sample_airplane()

    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": datetime.datetime(2024, 4, 4, 14, 45),
        "arrival_time": datetime.datetime(2024, 4, 5, 14, 45)
    }
    defaults.update(params)

    return Flight.objects.create(**defaults)


def sample_order(**params):
    if not params.get("user"):
        user = sample_user()
    else:
        user = params.get("user")

    defaults = {"user": user}
    defaults.update(params)

    return Order.objects.create(**defaults)


def sample_ticket(**params):
    flight = params.get("flight", sample_flight())

    if not params.get("order"):
        order = sample_order()
    else:
        order = params.get("order")

    defaults = {
        "row": 1,
        "seat": 1,
        "flight": flight,
        "order": order
    }
    defaults.update(params)

    return Ticket.objects.create(**defaults)
