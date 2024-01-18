from rest_framework import serializers

from theatre.models import (TheatreHall,
                            Reservation,
                            Actor,
                            Genre,
                            Play,
                            Performance,
                            Ticket)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class ActorListSerializer(ActorSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name",)


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title", "description", "actor", "genre")


class PlayDetailSerializer(PlaySerializer):
    actor = ActorSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)


class PlayListSerializer(PlaySerializer):
    actor = ActorListSerializer(many=True, read_only=True)
    genre = GenreListSerializer(many=True, read_only=True)


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("name", "rows", "seats_in_row")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class PerformanceListSerializer(PerformanceSerializer):
    play = PlayListSerializer(many=False, read_only=True)
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name",
        read_only=True
    )

    class Meta:
        model = Performance
        fields = ("id", "theatre_hall_name", "show_time", "play")


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayDetailSerializer(many=False, read_only=True)
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name",
        read_only=True
    )

    class Meta:
        model = Performance
        fields = ("id", "theatre_hall_name", "show_time", "play")


class ReservationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.username",
                                        read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "name")


class TicketSerializer(serializers.ModelSerializer):
    theatre_hall_name = serializers.CharField(
        source="performance.theatre_hall.name",
        read_only=True
    )
    user_name = serializers.CharField(
        source="reservation.user.username",
        read_only=True
    )
    show_time = serializers.CharField(
        source="performance.show_time",
        read_only=True
    )
    reservation = ReservationSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "theatre_hall_name",
            "user_name",
            "show_time",
            "reservation"
        )
