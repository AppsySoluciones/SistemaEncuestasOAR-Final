from django import forms
from .models import Encuesta

class EncuestaForm(forms.ModelForm):
    mesa = forms.CharField(required=False)
    puesto = forms.CharField(required=False)
    class Meta:
        model = Encuesta
        
        fields = ['nombres', 'apellidos', 'fecha_nacimiento', 'genero', 'cedula', 'celular', 'email', 'zona', 'direccion', 'barrio', 'escolaridad', 'ocupacion', 'tipo_recoleccion', 'ciudad_votacion','mesa','puesto']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'fecha_nacimiento': 'Fecha de nacimiento (YYYY-MM-DD)',
        }
        

