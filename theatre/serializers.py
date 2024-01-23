from django.db import transaction
from rest_framework import serializers

from theatre.models import (
    TheatreHall,
    Reservation,
    Actor,
    Genre,
    Play,
    Performance,
    Ticket,
)


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("first_name", "last_name")


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title", "description", "actor", "genre")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class GenreListSerializer(GenreSerializer):
    plays_title = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="title", source="genre_plays"
    )

    class Meta:
        model = Genre
        fields = ("name", "plays_title")


class ActorListSerializer(ActorSerializer):
    plays_title = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="title", source="actor_plays"
    )

    class Meta:
        model = Actor
        fields = ("id", "full_name", "plays_title")


class PlayDetailSerializer(PlaySerializer):
    actor = ActorListSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    theatre_hall_name = serializers.CharField(
        source="performance_play.performance.name", read_only=True
    )

    class Meta:
        model = Play
        fields = ("title",
                  "actor",
                  "genre",
                  "description",
                  "theatre_hall_name")


class PlayListSerializer(PlaySerializer):
    actor = ActorSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)


class ActorDetailSerializer(ActorSerializer):
    actor_plays = PlayListSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "actor_plays")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class PerformanceListSerializer(PerformanceSerializer):
    play = PlayDetailSerializer(many=False, read_only=True)
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name", read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Performance
        fields = (
            "id",
            "theatre_hall_name",
            "show_time",
            "play",
            "tickets_available"
        )


class TicketSerializer(serializers.ModelSerializer):
    theatre_hall_name = serializers.CharField(
        source="performance.theatre_hall.name"
    )
    user_name = serializers.CharField(source="reservation.user.username")
    show_time = serializers.CharField(source="performance.show_time")

    class Meta:
        model = Ticket
        fields = ("id",
                  "row",
                  "seat",
                  "theatre_hall_name",
                  "user_name",
                  "show_time")


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat")


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayListSerializer(many=False, read_only=True)
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name", read_only=True
    )
    taken_places = TicketSeatsSerializer(
        source="tickets", many=True, read_only=True
    )

    class Meta:
        model = Performance
        fields = (
            "id",
            "theatre_hall_name",
            "show_time",
            "play",
            "taken_places"
        )


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True,
                               read_only=False,
                               allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation
