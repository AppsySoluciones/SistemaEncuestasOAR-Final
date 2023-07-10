import django_tables2 as tables
from django.contrib.auth.models import User
from .models import Encuesta
import datetime
from django.utils.timezone import now

import datetime
import django_tables2 as tables

class EdadColumn(tables.Column):
    def render(self, value):
        today = datetime.date.today()
        age = today.year - value.year
        if today.month < value.month or (today.month == value.month and today.day < value.day):
            age -= 1
        return age

class EncuestaTable(tables.Table):
    usuario = tables.Column(verbose_name='Usuario')
    edad = EdadColumn(verbose_name='Edad', accessor='fecha_nacimiento')

    class Meta:
        model = Encuesta
        fields = ('nombres', 'apellidos', 'fecha_nacimiento', 'genero', 'cedula', 'celular', 'email', 'zona', 'direccion', 'barrio', 'escolaridad', 'ocupacion', 'tipo_recoleccion', 'ciudad_votacion', 'puesto', 'mesa', 'usuario', 'edad')
        template_name = 'django_tables2/bootstrap4.html'






