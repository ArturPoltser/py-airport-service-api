from django.contrib import admin

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


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super(AirplaneAdmin, self).get_queryset(request)
        return queryset.select_related("airplane_type")


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super(RouteAdmin, self).get_queryset(request)
        return queryset.select_related("source", "destination")


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super(FlightAdmin, self).get_queryset(request)
        return queryset.select_related(
            "route__source",
            "route__destination",
            "airplane"
        )


admin.site.register(Crew)
admin.site.register(AirplaneType)
admin.site.register(Airport)
