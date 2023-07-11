from django.urls import path
from .views import formulario_registro, exito_registro, encuesta_list, editar_encuesta, eliminar_encuesta, home, enviar_correo_cumpleanios
from .views import dashboard, CustomLoginView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('home/',home,name='home'),
    path('registro/', formulario_registro, name='formulario_registros'),
    path('exito_registro/', exito_registro, name='exito_registro'),
    path('encuesta_list/', encuesta_list, name='encuesta_list'),
    path('encuesta/editar/<int:pk>/', editar_encuesta, name='editar_encuesta'),
    path('encuesta/eliminar/<int:pk>/', eliminar_encuesta, name='eliminar_encuesta'),
    path('dashboard/', dashboard, name='dashboard'),
    path('send_email',enviar_correo_cumpleanios,name='send_email')
    
]
