from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from .views import ReservationCreateView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hotovo/$', TemplateView.as_view(template_name='hotovo.html')),
    url(r'^$', ReservationCreateView.as_view(template_name='home.html')),
)

