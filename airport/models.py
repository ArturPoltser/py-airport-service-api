from django.contrib.auth import get_user_model
from django.db import models

from airport.choises import CREW_POSITION_TYPE


class Crew(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    position = models.CharField(max_length=63, choices=CREW_POSITION_TYPE)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.full_name} - {self.position}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        verbose_name = "Airplane Type"
        verbose_name_plural = "Airplane Types"

    def __str__(self) -> str:
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=63)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.PROTECT,
        related_name="airplanes"
    )

    def __str__(self) -> str:
        return f"Airplane: {self.name}, Type: {self.airplane_type}"


class Airport(models.Model):
    name = models.CharField(max_length=63)
    closest_big_city = models.CharField(max_length=63)

    def __str__(self) -> str:
        return f"{self.name} - {self.closest_big_city}"


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="source_routes"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="destination_routes"
    )
    distance = models.PositiveIntegerField()

    class Meta:
        unique_together = ("source", "destination")

    def __str__(self) -> str:
        return f"{self.source.name}-{self.destination.name}"


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="flights")

    def __str__(self) -> str:
        return f"{self.route} - {self.airplane.name}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Order #{self.id}: {self.created_at}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]

    def __str__(self) -> str:
        return f"{self.flight} (row: {self.row}, seat: {self.seat})"
