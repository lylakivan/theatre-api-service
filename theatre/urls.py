from django.urls import path, include
from rest_framework import routers

from theatre.views import (
    GenreViewSet,
    ActorViewSet,
    TheatreHallViewSet,
    PlayViewSet,
    ReservationViewSet,
    PerformanceViewSet,
    # TicketViewSet,
)


router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("theatre_hall", TheatreHallViewSet)
router.register("plays", PlayViewSet)
router.register("reservation", ReservationViewSet)
router.register("performance", PerformanceViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "theatre"
