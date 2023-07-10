from django.db import models
from django.contrib.auth.models import User

class Encuesta(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10)
    cedula = models.CharField(max_length=20, unique=True)
    celular = models.CharField(max_length=20)
    email = models.EmailField()
    zona = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    barrio = models.CharField(max_length=100)
    escolaridad = models.CharField(max_length=50)
    ocupacion = models.CharField(max_length=100)
    tipo_recoleccion = models.CharField(max_length=50)
    ciudad_votacion = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    mesa = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
