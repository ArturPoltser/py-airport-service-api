from rest_framework import routers

from airport.views import CrewViewSet, AirplaneTypeViewSet


router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("airplane_types", AirplaneTypeViewSet)

urlpatterns = router.urls

app_name = "airport"
