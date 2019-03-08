from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.usuarios.models import *
from apps.usuarios.forms import *
from django.contrib import messages


# Dashboard
def home(request):
    return render(request, 'usuarios/home.html')


# Crear usuario
def crear_usuario(request):

    # Usuario que hizo la peticion a la funcion (usuario que esta en la sesion)
    usuario = request.user

    # Validacion para cargo del usuario (is_staff)
    if True:
        if request.method == 'POST':
            # Crea el formulario a partir de los datos del request
            form = CrearUsuarioForm(request.POST)
            # Verifica si el formulario es valido de acuerdo a los tipos de datos del form
            if form.is_valid():
                # Guarda la instancia del modelo que referencia el formualario
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

    # En caso de que el usuario no sea admin se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('usuarios:home')


# Editar usuario
def editar_usuario(request, id_usuario):
    usuario = request.user
    usuario_editar = Usuario.objects.get(id=id_usuario)

    if usuario.is_staff:
        if request.method == 'POST':
            form = EditarUsuarioForm(request.POST, instance=usuario_editar)
            if form.is_valid():
                form.save()
                messages.success(request, 'Has modificado el usuario exitosamente!')
                return redirect('usuarios:home')
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'usuarios/editar_usuario.html', {'form': form})
        else:
            form = EditarUsuarioForm(instance=usuario_editar)
            return render(request, 'usuarios/editar_usuario.html', {'form': form})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('usuarios:home')


# Crear cargo
def crear_cargo(request):
    usuario = request.user

    if usuario.is_staff:
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
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('usuarios:home')


# Editar cargo
def editar_cargo(request, id_cargo):
    usuario = request.user
    cargo = Cargo.objects.get(id=id_cargo)

    if usuario.is_staff:
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
            form = CrearCargoForm()
            return render(request, 'usuarios/crear_cargo.html', {'form': form})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('usuarios:home')
