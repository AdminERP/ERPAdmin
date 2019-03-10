from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from apps.usuarios.forms import *
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import update_session_auth_hash


# Dashboard
def home(request):
    if request.user.is_superuser:
        return render(request, 'usuarios/home.html')
    else:
        return render(request, 'usuarios/home_aux.html')


# Crear usuario
@permission_required('usuario.add_usuario', raise_exception=True)
def crear_usuario(request):

    if request.method == 'POST':

        # Crea el formulario a partir de los datos del request
        form = CrearUsuarioForm(request.POST)

        # Verifica si el formulario es valido de acuerdo a los tipos de datos del form
        if form.is_valid():

            # Guarda la instancia del modelo que referencia el formulario
            form.save()
            messages.success(request, 'Usuario creado exitosamente')
            return render(request, 'usuarios/crear_usuario.html', {'form': CrearUsuarioForm()})
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'usuarios/crear_usuario.html', {'form': form})

        # Caso cuando el request es un GET
    else:
        form = CrearUsuarioForm()
        return render(request, 'usuarios/crear_usuario.html', {'form': form})


# Editar usuario
@permission_required('usuario.change_usuario', raise_exception=True)
def editar_usuario(request, id_usuario):
    usuario_editar = Usuario.objects.get(id=id_usuario)
    nombre_usuario_editar = usuario_editar.get_full_name()
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario_editar)
        if form.is_valid():
            form.save()
            messages.success(request, 'Has modificado el usuario exitosamente!')
            return redirect('usuarios:home')
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'usuarios/editar_usuario.html', {'form': form, 'nombre_usuario_editar':
                nombre_usuario_editar})
    else:
        form = EditarUsuarioForm(instance=usuario_editar)
        return render(request, 'usuarios/editar_usuario.html', {'form': form, 'nombre_usuario_editar':
                                                                               nombre_usuario_editar})


# Editar password
@login_required
def editar_password(request):
    form = EditarPasswordForm(user=request.user)
    if request.method == 'POST':
        form = EditarPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Contraseña guardada exitosamente!')
            return redirect('usuarios:home')
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'usuarios/editar_password.html', {'form': form})
    else:
        return render(request, 'usuarios/editar_password.html', {'form': form})


# Reestablecer password
@permission_required('usuario.change_password', raise_exception=True)
def reestablecer_password(request, id_usuario):
    usuario_editar = Usuario.objects.get(id=id_usuario)
    nombre_usuario_editar = usuario_editar.get_full_name()
    form = SetPasswordForm(user=usuario_editar)
    if request.method == 'POST':
        form = SetPasswordForm(user=usuario_editar, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Has modificado la contraseña exitosamente!')
            return redirect('usuarios:consultar_usuarios')
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'usuarios/reestablecer_password.html', {'form': form,
                                                                           'nombre_usuario_editar':
                                                                               nombre_usuario_editar})
    else:
        return render(request, 'usuarios/reestablecer_password.html', {'form': form, 'nombre_usuario_editar':
            nombre_usuario_editar})


# Activar/Desactivar usuario
@permission_required('usuario.activate_usuario', raise_exception=True)
def activar_usuario(request):
    if request.is_ajax():
        id_usuario = request.POST.get('id_usuario', None)
        try:
            usuario_editar = Usuario.objects.get(id=id_usuario)
            if usuario_editar.is_active:
                usuario_editar.is_active = False
            else:
                usuario_editar.is_active = True
            usuario_editar.save()
            return JsonResponse({'nombre_usuario': usuario_editar.get_full_name()})
        except Usuario.DoesNotExist:
            return JsonResponse({'response': 0})


# Consultar usuarios
@permission_required('usuario.view_usuarios', raise_exception=True)
def consultar_usuarios(request):
    if request.method == 'GET':
        return render(request, 'usuarios/consultar_usuarios.html', {'usuarios': Usuario.consultar_usuarios()})


# Crear cargo
@permission_required('cargo.add_cargo', raise_exception=True)
def crear_cargo(request):
    if request.method == 'POST':
        form = CrearCargoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo creado exitosamente!')
            return redirect('usuarios:home')
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'usuarios/crear_cargo.html', {'form': form})
    else:
        form = CrearCargoForm()
        return render(request, 'usuarios/crear_cargo.html', {'form': form})


# Editar cargo
@permission_required('cargo.change_cargo', raise_exception=True)
def editar_cargo(request, id_cargo):
    cargo = Cargo.objects.get(id=id_cargo)
    if request.method == 'POST':
        form = CrearCargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo modificado exitosamente!')
            return redirect('usuarios:home')
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'usuarios/crear_cargo.html', {'form': form})
    else:
        form = CrearCargoForm(instance=cargo)
        return render(request, 'usuarios/crear_cargo.html', {'form': form})


# Consultar cargos
@permission_required('cargo.view_cargos', raise_exception=True)
def consultar_cargos(request):
    if request.method == 'GET':
        return render(request, 'usuarios/consultar_cargos.html', {'cargos': Cargo.consultar_cargos()})
