from django.contrib.auth import views as auth_views
from django.urls import path

from apps.usuarios.views import *

app_name = 'usuarios'

urlpatterns = [
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='usuarios/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home', home, name='home'),
    path('crear-usuario', crear_usuario, name='crear_usuario'),
    path('editar-usuario/<int:id_usuario>', editar_usuario, name='editar_usuario'),
    path('consultar-usuarios', consultar_usuarios, name='consultar_usuarios'),
    path('api/activar-usuario', activar_usuario, name='activar_usuario'),
    path('crear-cargo', crear_cargo, name='crear_cargo'),
    path('editar-cargo/<int:id_cargo>', editar_cargo, name='editar_cargo'),
    path('consultar-cargos', consultar_cargos, name='consultar_cargos'),
    path('editar-password', editar_password, name='editar_password'),
    path('reestablecer-password/<int:id_usuario>', reestablecer_password, name='reestablecer_password'),
]
