from django.shortcuts import render, redirect
from apps.usuarios.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import permission_required


# Dashboard
def home(request):
    return render(request, 'usuarios/home.html')


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
