# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Reservation(models.Model):
    slug        = models.SlugField(editable=False)
    created     = models.DateTimeField(auto_now_add=True)
    name        = models.CharField('jméno', max_length=100)
    phone       = models.CharField('telefon', max_length=15)
    email       = models.EmailField('e-mail')

    def __str__(self):
        return self.name

    @property
    def price(self):
        return sum(rs.price for rs in self.seats.all())



@python_2_unicode_compatible
class Seat(models.Model):
    ROOMS = {
        'S': 'Sál',
        'G': 'Galerie',
    }
    room        = models.CharField(max_length=1, choices=ROOMS.items(), editable=False)
    table       = models.IntegerField(editable=False)
    seat        = models.IntegerField(editable=False)

    class Meta:
        ordering            = ('room', 'table', 'seat')
        unique_together     = (('room', 'table', 'seat'),)

    def __str__(self):
        return '{room}{table}/{seat}'.format(
            room    = self.room,
            table   = self.table,
            seat    = self.seat,
        )

    @property
    def room_name(self):
        return self.ROOMS[self.room]



@python_2_unicode_compatible
class ReservationSeat(models.Model):
    STUDENT = 'S'
    OTHER   = 'O'
    VARIANTS = {
        STUDENT:    'student',
        OTHER:      'ostatní',
    }
    PRICES = {
        STUDENT:    100,
        OTHER:      120,
    }
    reservation = models.ForeignKey(Reservation, related_name='seats')
    seat        = models.OneToOneField(Seat, related_name='reservation', unique=True)
    variant     = models.CharField(max_length=1, choices=VARIANTS.items())

    class Meta:
        ordering            = ('seat__room', 'seat__table', 'seat__seat')

    def __str__(self):
        return '{reservation}, {seat}, {variant}'.format(
            reservation = self.reservation,
            seat        = self.seat,
            variant     = self.VARIANTS[self.variant],
        )

    @property
    def variant_name(self):
        return self.VARIANTS[self.variant]

    @property
    def price(self):
        return self.PRICES[self.variant]

