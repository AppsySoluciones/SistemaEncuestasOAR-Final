"""
URL configuration for sitemaencuestas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.shortcuts import render,redirect
from django.conf import settings
from django.core.mail import send_mail
URL_SERVER = settings.BACKEND_URL

class CustomLoginView(LoginView):
    template_name = 'pages/login.html'
    success_url = f'{URL_SERVER}/encuesta_list/'
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
        return redirect(f'{URL_SERVER}/login')
    
def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect(f'{URL_SERVER}/login') 


    
from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(('Encuesta.urls','Encuesta'))),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    
]
