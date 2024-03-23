from rest_framework import routers

from airport.views import (
    CrewViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    AirportViewSet,
    RouteViewSet,
    FlightViewSet,
)

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airports", AirportViewSet)
router.register("routs", RouteViewSet)
router.register("flights", FlightViewSet)

urlpatterns = router.urls

app_name = "airport"
