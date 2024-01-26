from django.contrib import admin

from theatre.models import (
    Ticket,
    Performance,
    Play,
    Genre,
    Actor,
    Reservation,
    TheatreHall
)


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    inlines = (TicketInline, )


admin.site.register(TheatreHall)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Play)
admin.site.register(Performance)
admin.site.register(Ticket)
