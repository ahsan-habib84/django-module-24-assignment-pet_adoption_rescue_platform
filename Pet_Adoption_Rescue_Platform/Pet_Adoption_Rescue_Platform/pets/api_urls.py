from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api import AdoptionRequestViewSet, CustomObtainAuthToken, PetViewSet

router = DefaultRouter()
router.register("pets", PetViewSet, basename="api-pets")
router.register("adoptions", AdoptionRequestViewSet, basename="api-adoptions")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", CustomObtainAuthToken.as_view(), name="api-token"),
]
