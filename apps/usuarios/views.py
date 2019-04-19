from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.http.response import JsonResponse
from django.shortcuts import render, redirect

from apps.usuarios.forms import *


# Dashboard
@login_required()
def home(request):
    return render(request, 'usuarios/home.html')


# Crear usuario
@permission_required('usuarios.add_usuario', raise_exception=True)
def crear_usuario(request):
    if request.method == 'POST':

        # Crea el formulario a partir de los datos del request
        form = CrearUsuarioForm(request.POST)

        # Verifica si el formulario es valido de acuerdo a los tipos de datos del form
        if form.is_valid():

            # Obtiene el cargo
            cargo = form.cleaned_data['cargo']
            user = form.save(commit=False)

            # Crea el usuario
            user.save()

            # Agrega el usuario al grupo y lo guarda
            user.groups.add(cargo)
            user.save()

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
@permission_required('usuarios.change_usuario', raise_exception=True)
def editar_usuario(request, id_usuario):
    usuario_editar = Usuario.objects.get(id=id_usuario)
    nombre_usuario_editar = usuario_editar.get_full_name()
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario_editar)
        if form.is_valid():

            # Obtiene el cargo
            cargo = form.cleaned_data['cargo']
            user = form.save(commit=False)

            # Actualiza el grupo y lo guarda
            user.groups.clear()
            user.groups.add(cargo)
            user.save()

            messages.success(request, 'Has modificado el usuario exitosamente!')
            return redirect('usuarios:consultar_usuarios')
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'usuarios/editar_usuario.html', {'form': form,
                                                                    'nombre_usuario_editar': nombre_usuario_editar})
    else:
        form = EditarUsuarioForm(instance=usuario_editar)
        return render(request, 'usuarios/editar_usuario.html', {'form': form,
                                                                'nombre_usuario_editar': nombre_usuario_editar})


# Editar password
@login_required
def editar_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
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
@permission_required('usuarios.change_password', raise_exception=True)
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
            return render(request, 'usuarios/reestablecer_password.html',
                          {'form': form, 'nombre_usuario_editar': nombre_usuario_editar})
    else:
        return render(request, 'usuarios/reestablecer_password.html',
                      {'form': form, 'nombre_usuario_editar': nombre_usuario_editar})


# Activar/Desactivar usuario
@permission_required('usuarios.activate_usuario', raise_exception=True)
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
            return JsonResponse({'nombre_usuario': usuario_editar.get_full_name(), 'estado': usuario_editar.is_active})
        except Usuario.DoesNotExist:
            return JsonResponse({'response': 0})


# Consultar usuarios
@permission_required('usuarios.view_usuarios', raise_exception=True)
def consultar_usuarios(request):
    if request.method == 'GET':
        return render(request, 'usuarios/consultar_usuarios.html', {'usuarios': Usuario.consultar_usuarios(), 'action': 'list'})


# Crear cargo
@permission_required('usuarios.add_cargo', raise_exception=True)
def crear_cargo(request):
    if request.method == 'POST':
        form = CrearCargoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo creado exitosamente!')
            return redirect('usuarios:consultar_cargos')
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'usuarios/crear_cargo.html', {'form': form})
    else:
        form = CrearCargoForm()
        return render(request, 'usuarios/crear_cargo.html', {'form': form})


# Editar cargo
@permission_required('usuarios.change_cargo', raise_exception=True)
def editar_cargo(request, id_cargo):
    cargo = Cargo.objects.get(id=id_cargo)
    nombre_cargo = cargo.name
    id_cargo = cargo.id
    if request.method == 'POST':
        form = EditarCargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo modificado exitosamente!')
            return redirect('usuarios:consultar_cargos')
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'usuarios/editar_cargo.html', {'form': form, 'nombre_cargo': nombre_cargo,
                                                                  'id_cargo': id_cargo})
    else:
        form = EditarCargoForm(instance=cargo)
        return render(request, 'usuarios/editar_cargo.html', {'form': form, 'nombre_cargo': nombre_cargo,
                                                              'id_cargo': id_cargo})


# Consultar cargos
@permission_required('usuarios.view_cargos', raise_exception=True)
def consultar_cargos(request):
    if request.method == 'GET':
        return render(request, 'usuarios/consultar_cargos.html', {'cargos': Cargo.consultar_cargos()})
