from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Encuesta
from .forms import EncuestaForm
from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import Encuesta
from .tables import EncuestaTable
from .filters import EncuestaFilter
from django.conf import settings
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import HttpResponse
from django.db.models import F, ExpressionWrapper
from django.db.models.functions import ExtractYear
from django.db import models
import datetime


BACKEND_URL = settings.BACKEND_URL

@login_required(login_url=reverse_lazy('login'))
def home(request):
    return render(request, 'index.html')

@login_required
def formulario_registro(request):
    if request.user.groups.filter(name__in=['Registrar','Administrar','Editar']).exists():
        if request.method == 'POST':
            form = EncuestaForm(request.POST)
            if form.is_valid():
                encuesta = form.save(commit=False)
                encuesta.usuario = request.user
                encuesta.save()
                messages.success(request, 'La encuesta se ha registrado correctamente.')
                return redirect(f'{BACKEND_URL}/registro/')
            print(form.errors)
            messages.error(request, form.errors)
        else:
            
            form = EncuestaForm()

        # Verificar el rol del usuario
        '''  if request.user.groups.filter(name='Editar').exists():
            form.fields['mesa'].widget = forms.TextInput(attrs={'placeholder': 'Ingrese el número de mesa'})
            form.fields['puesto'].widget = forms.TextInput(attrs={'placeholder': 'Ingrese el número de puesto'}) '''
        
        context = {'form': form, 'URL_BACKEND': BACKEND_URL}
        return render(request, 'formulario_registro.html', context)
    else:
        return render(request, 'no_autorizado.html')


@login_required
def exito_registro(request):
    return render(request, 'exito_registro.html')
@login_required
def encuesta_list(request):
    user = request.user
    if request.user.groups.filter(name__in=['Administrar','Editar','Consultar']).exists():
        encuesta_filter = EncuestaFilter(request.GET, queryset=Encuesta.objects.all())
    elif request.user.groups.filter(name='Registrar').exists():
        encuesta_filter = EncuestaFilter(request.GET, queryset=Encuesta.objects.filter(usuario=user))
    else:
        return render(request, 'no_autorizado.html')

    # Aplica el filtro
    filtered_data = encuesta_filter.qs

    table = EncuestaTable(filtered_data)
    RequestConfig(request).configure(table)

    return render(request, 'encuesta_list.html', {'table': table, 'encuesta_filter': encuesta_filter, 'URL_BACKEND': BACKEND_URL, 'today': date.today()})


@login_required
def editar_encuesta(request, pk):
    if request.user.groups.filter(name__in=['Administrar','Editar']).exists():
        encuesta = get_object_or_404(Encuesta, pk=pk)
        if request.method == 'POST':
            form = EncuestaForm(request.POST, instance=encuesta)
            if form.is_valid():
                form.save()
                messages.success(request, 'La encuesta se ha actualizado correctamente.')
                return redirect(f'{BACKEND_URL}/encuesta_list/')
            print(form.errors)
        else:
            # Pasar los valores de "mesa" y "puesto" en el contexto
            form = EncuestaForm(instance=encuesta)
            form.initial['fecha_nacimiento'] = encuesta.fecha_nacimiento.strftime('%Y-%m-%d')  # Establecer el valor inicial de fecha_nacimiento
            context = {
                'form': form,
                'mesa_value': encuesta.mesa,
                'puesto_value': encuesta.puesto,
            }
            return render(request, 'editar_encuesta.html', context)
    else:
        return render(request, 'no_autorizado.html') 




@login_required
def eliminar_encuesta(request, pk):
    if request.user.groups.filter(name='Administrar').exists():
        encuesta = get_object_or_404(Encuesta, pk=pk)
        if request.method == 'POST':
            encuesta.delete()
            # Redirigir a la página de éxito o hacer cualquier otra acción necesaria
            return redirect(f'{BACKEND_URL}/encuesta_list/')
        return render(request, 'eliminar_encuesta.html', {'encuesta': encuesta,'URL_BACKEND':BACKEND_URL})
    else:
        return render(request, 'no_autorizado.html', {'URL_BACKEND':BACKEND_URL})
    
@login_required
def dashboard(request):
        # Definir los grupos de edad
        grupos_edad = [(18, 25), (26, 35), (36, 45), (46, 55), (56, 65), (66, 75), (76, 90)]
        grupos_edad_count = []
        # Obtener la fecha actual
        fecha_actual = datetime.date.today()

        # Iterar sobre los grupos de edad y contar los registros correspondientes
        # Iterar sobre los grupos de edad y contar los registros correspondientes
        for grupo in grupos_edad:
            edad_min, edad_max = grupo
            # Calcular la fecha mínima y máxima de nacimiento para el grupo de edad
            fecha_min = fecha_actual - datetime.timedelta(days=edad_max * 365)
            fecha_max = fecha_actual - datetime.timedelta(days=edad_min * 365)
            # Filtrar los registros por fecha de nacimiento en el rango especificado
            num_registros = Encuesta.objects.filter(fecha_nacimiento__gte=fecha_min, fecha_nacimiento__lt=fecha_max).count()
            grupos_edad_count.append(num_registros*10)
            
            
        total = Encuesta.objects.count()
        presencial = Encuesta.objects.filter(tipo_recoleccion='presencial').count()
        virtual = Encuesta.objects.filter(tipo_recoleccion='virtual').count()
        porcentaje_total = total
        num_masculinos = Encuesta.objects.filter(genero='masculino').count()
        num_femeninos = Encuesta.objects.filter(genero='femenino').count()

        rural = Encuesta.objects.filter(zona='rural').count()
        urbano = Encuesta.objects.filter(zona='urbana').count()
        if porcentaje_total == 0:
            porcentaje_total = 1
        context = {
            'num_masculinos':round(num_masculinos*100/porcentaje_total),
            'num_femeninos':round(num_femeninos*100/porcentaje_total),
            'URL_BACKEND':BACKEND_URL,
            'total_encuestas':total,
            'virtual':virtual,
            'presencial':presencial,
            'grupos_edad_count': grupos_edad_count,
            'rural':round(100*rural/porcentaje_total),
            'urbano':round(100*urbano/porcentaje_total),
            }
        return render(request, 'dashboard-influencer.html',context=context)

def enviar_correo_cumpleanios(request):
    # Configuración del servidor SMTP de Gmail
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    email_sender = 'crecentosuperadm@gmail.com'
    email_password = 'eoarbytsitgtzdaz'

    # Obtén la fecha de hoy
    hoy = date.today()

    # Filtra las encuestas cuyo cumpleaños es hoy
    encuestas_hoy = Encuesta.objects.filter(fecha_nacimiento__month=hoy.month, fecha_nacimiento__day=hoy.day)

    # Envía el correo electrónico a cada destinatario
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(email_sender, email_password)
        for encuesta in encuestas_hoy:
            destinatario = encuesta.email

            # Crea el mensaje de correo electrónico
            mensaje = MIMEMultipart()
            mensaje['From'] = email_sender
            mensaje['To'] = destinatario
            mensaje['Subject'] = 'Feliz cumpleaños!'
            
            # Cuerpo del mensaje
            texto = f'¡Feliz cumpleaños, {encuesta.nombres}! Esperamos que tengas un día maravilloso.'
            mensaje.attach(MIMEText(texto, 'plain'))

            # Envía el correo electrónico
            server.sendmail(email_sender, destinatario, mensaje.as_string())

    # Retorna una respuesta HTTP indicando que los correos electrónicos han sido enviados
    return HttpResponse('Correo electrónico de cumpleaños enviado correctamente.')




class CustomLoginView(LoginView):
    template_name = 'pages/login.html'
    success_url = f'{settings.BACKEND_URL}/encuesta_list/'
    a =0

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        # Realiza el inicio de sesión y redirige a la página de éxito
        self.request.session['username'] = form.cleaned_data['username']
        user = form.get_user()
        from django.contrib.auth import login
        login(self.request, user)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # Maneja los errores si el formulario no es válido
        return self.render_to_response('/')
    
def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect(f'{settings.BACKEND_URL}/login') 