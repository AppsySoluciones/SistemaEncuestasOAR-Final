import django_filters
from django import forms
from .models import Encuesta

class EncuestaFilter(django_filters.FilterSet):
    zona = django_filters.CharFilter(field_name='zona', label='Zona', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la zona'}))
    genero = django_filters.ChoiceFilter(field_name='genero', label='Género', choices=(('masculino','Masculino'),('femenino','Femenino')), widget=forms.Select(attrs={'class': 'form-control'}))
    barrio = django_filters.CharFilter(field_name='barrio', label='Barrio', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el barrio'}))
    ciudad_votacion = django_filters.CharFilter(field_name='ciudad_votacion', label='Ciudad de votación', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la ciudad de votación'}))
    tipo_recoleccion = django_filters.ChoiceFilter(field_name='tipo_recoleccion', label='Tipo de recolección', choices=(('virtual','Virtual'),('presencial','Presencial')), widget=forms.Select(attrs={'class': 'form-control'}))
    escolaridad = django_filters.ChoiceFilter(field_name='escolaridad', label='Nivel de escolaridad', choices=(('primaria','Primaria'),('secundaria','Secundaria'),('universitaria','Universitaria')), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Encuesta
        fields = []

