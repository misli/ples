# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

from django.contrib import admin
from django.db.models import Count

from .models import Reservation, Seat, ReservationSeat


class ReservationSeatInlineAdmin(admin.TabularInline):
    model = ReservationSeat
    extra = 0

class ReservationAdmin(admin.ModelAdmin):
    list_display    = ('created', 'name', 'phone', 'email', 'num_seats')
    search_fields   = ('name', 'phone', 'email')
    inlines         = (ReservationSeatInlineAdmin,)

    def get_queryset(self, request):
        return super(ReservationAdmin, self).get_queryset(request).annotate(num_seats=Count('seats'))

    def num_fixture_metas_count(self, obj):
      return obj.num_fixture_metas
    num_fixture_metas_count.short_description = 'Fixture Count'
    num_fixture_metas_count.admin_order_field = 'num_fixture_metas'

    def num_seats(self, obj):
        return obj.num_seats
    num_seats.admin_order_field = 'num_seats'

admin.site.register(Reservation, ReservationAdmin)



class SeatAdmin(admin.ModelAdmin):
    list_display    = ('room', 'table', 'seat', 'reservation')
    search_fields   = ('reservation__reservation__name', 'reservation__reservation__phone', 'reservation__reservation__email')

admin.site.register(Seat, SeatAdmin)

