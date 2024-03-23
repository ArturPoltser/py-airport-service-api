from rest_framework import routers

from airport.views import CrewViewSet
router = routers.DefaultRouter()
router.register("crews", CrewViewSet)

urlpatterns = router.urls

app_name = "airport"
