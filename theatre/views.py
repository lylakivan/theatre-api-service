from django.db.models import F, Count
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from theatre.models import (
    TheatreHall,
    Reservation,
    Actor,
    Genre,
    Play,
    Performance,
    Ticket
)
from theatre.serializers import (
    TheatreHallSerializer,
    ReservationSerializer,
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    PerformanceSerializer,
    TicketSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    PlayListSerializer,
    PlayDetailSerializer,
)


class Pagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == "list":
            return ActorListSerializer
        if self.action == "retrieve":
            return ActorDetailSerializer
        return ActorSerializer


class GenreViewSet(viewsets.ViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer
    pagination_class = Pagination


    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the plays with filters"""
        queryset = self.queryset

        title = self.request.query_params.get("title")
        actors = self.request.query_params.get("actor")
        genres = self.request.query_params.get("genre")

        if title:
            queryset = queryset.filter(title__icontains=title)

        if actors:
            actors_ids = self._params_to_ints(actors)
            queryset = queryset.filter(actor__id__in=actors_ids)

        if genres:
            genres_ids = self._params_to_ints(genres)
            queryset = queryset.filter(genre__id__in=genres_ids)

        if self.action in ("retrieve", "list"):
            queryset = queryset.prefetch_related("actor", "genre")

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayDetailSerializer
        return PlaySerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ("retrieve", "list"):
            queryset = (
                queryset
                .select_related("play", "theatre_hall")
                .annotate(
                    tickets_available=(
                        F("theatre_hall__rows")
                        * F("theatre_hall__seats_in_row")
                        - Count("tickets")
                    )
                )
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        return PerformanceSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return Reservation.objects.select_related("user").filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
