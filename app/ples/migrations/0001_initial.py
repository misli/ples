# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100, verbose_name='jm\xe9no')),
                ('phone', models.CharField(max_length=15, verbose_name='telefon')),
                ('email', models.EmailField(max_length=75, verbose_name='e-mail')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReservationSeat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('variant', models.CharField(max_length=1, choices=[('S', 'student'), ('O', 'ostatn\xed')])),
                ('reservation', models.ForeignKey(related_name='seats', to='ples.Reservation')),
            ],
            options={
                'ordering': ('seat__room', 'seat__table', 'seat__seat'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room', models.CharField(max_length=1, editable=False, choices=[('S', 'S\xe1l'), ('G', 'Galerie')])),
                ('table', models.IntegerField(editable=False)),
                ('seat', models.IntegerField(editable=False)),
            ],
            options={
                'ordering': ('room', 'table', 'seat'),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='seat',
            unique_together=set([('room', 'table', 'seat')]),
        ),
        migrations.AddField(
            model_name='reservationseat',
            name='seat',
            field=models.OneToOneField(related_name='reservation', to='ples.Seat'),
            preserve_default=True,
        ),
    ]
