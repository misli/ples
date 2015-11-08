# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

from django import forms
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import CreateView

from .models import Reservation, Seat, ReservationSeat


class ReservationCreateView(CreateView):
    model       = Reservation
    success_url = '/'

    def get_form(self, *args, **kwargs):
        form = super(ReservationCreateView, self).get_form(*args, **kwargs)
        for f in form.fields:
            form.fields[f].widget.attrs = {'class': 'form-control'}
        for seat in Seat.objects.filter(reservation=None):
            form.fields['seat-{}-variant'.format(seat.id)] = forms.fields.ChoiceField(
                choices     = ReservationSeat.VARIANTS.items(),
                required    = False,
                widget      = forms.HiddenInput,
            )
        return form

    def form_valid(self, form):
        response = super(ReservationCreateView, self).form_valid(form)
        reservation = self.object
        for key in form.cleaned_data:
            if key.startswith('seat') and form.cleaned_data[key]:
                rs = ReservationSeat()
                rs.reservation = reservation
                rs.seat = Seat.objects.get(id=int(key[5:-8]))
                rs.variant = form.cleaned_data[key]
                rs.save()
        message = render_to_string('mail.txt', {
            'reservation':  self.object,
        })
        send_mail(
            subject         = 'Rezervace míst na Skautský ples ve stylu MAFIE',
            message         = message,
            from_email      = '"Petr Lizna" <petr.lizna@ddmletovice.cz>',
            recipient_list  = (reservation.email,),
        )
        send_mail(
            subject         = 'Rezervace míst na Skautský ples ve stylu MAFIE',
            message         = message,
            from_email      = reservation.email,
            recipient_list  = ('"Petr Lizna" <petr.lizna@ddmletovice.cz>',),
        )
        return response

