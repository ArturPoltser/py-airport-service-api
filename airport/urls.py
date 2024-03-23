from rest_framework import routers

from airport.views import CrewViewSet, AirplaneTypeViewSet, AirplaneViewSet

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)

urlpatterns = router.urls

app_name = "airport"
