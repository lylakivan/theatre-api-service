from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Actor(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    actor = models.ManyToManyField(Actor, related_name="actor_plays")
    genre = models.ManyToManyField(Genre, related_name="genre_plays")


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(
        Play, on_delete=models.CASCADE, related_name="performance_play"
    )
    theatre_hall = models.ForeignKey(
        TheatreHall, on_delete=models.CASCADE, related_name="performance"
    )
    show_time = models.DateTimeField()


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservation"
    )

    def __str__(self):
        return f"{self.user.username}, created_at: {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(
        Performance,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ticket_performance",
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ticket_reservation",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat"],
                name="unique_ticket"
            )
        ]

    def clean(self) -> None:
        if not (1 <= self.row <= self.performance.theatre_hall.rows):
            raise ValidationError(
                {
                    "row": [
                        f"row number must be in available range:"
                        f" (1, {self.performance.theatre_hall.rows}):"
                    ]
                }
            )
        if not (1 <= self.seat <= self.performance.theatre_hall.seats_in_row):
            raise ValidationError(
                {
                    "seat": [
                        f"seat number must be in available range:"
                        f"(1, {self.performance.theatre_hall.seats_in_row})"
                    ]
                }
            )

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str = None,
        update_fields: list = None,
    ) -> None:
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{self.performance.play.title}, {self.row}, {self.seat}"
