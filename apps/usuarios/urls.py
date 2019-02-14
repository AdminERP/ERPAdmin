from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.usuarios.views import *

app_name = 'usuarios'

urlpatterns = [
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='usuarios/login.html'),
         name='login'),
    path('home', home, name='home')

]