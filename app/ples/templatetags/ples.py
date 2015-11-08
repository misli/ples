from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

from django import template

from ..models import Seat

register = template.Library()


@register.filter
def split(value):
    return value.split()


@register.inclusion_tag('seat.html', takes_context=True)
def seat(context, room, table):
    # this should not happen with valid template
    if room not in Seat.ROOMS:
        raise Exception('"{}" is not valid room'.format(room))
    if not table:
        raise Exception('"{}" is not valid table'.format(table))

    # use form.seat_counts to store counters
    # it is always the same with different copies of context
    if not hasattr(context['form'], 'seat_counts'):
        context['form'].seat_counts = {}
    rt = '{}-{}'.format(room, table)
    s  = context['form'].seat_counts[rt] = context['form'].seat_counts.get(rt, 0) + 1
    seat = Seat.objects.get_or_create(room=room, table=table, seat=s)[0]
    seat_context = {}
    seat_context['seat'] = seat
    try:
        seat_context['variant'] = context['form']['seat-{}-variant'.format(seat.id)]
    except KeyError:
        pass
    return seat_context

