from django.shortcuts import render, redirect
#from django.http import HttpResponse
from django.contrib import messages
from .forms import *
from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#autocomplete
from apps.usuarios.models import *
from apps.usuarios.forms import *
from django.http import HttpResponseRedirect, JsonResponse

def to_login(request):
    return redirect('/ordenes_servicio/login')

# Create your views here.
def ordenes_login(request):
    if request.user.is_authenticated:
        return redirect("/ordenes_servicio/welcome")
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/ordenes_servicio/welcome/")
        else:
            context = {"message":"Usuario o Contraseña Incorrectos"}
            return render(request, "usuarios/login.html",context)
    else:
        logout(request)
        return render(request, "usuarios/login.html")

def manage_options(request, context):
    context["options"] = [
        {"name": "Django Admin Site", "href": "/admin"},
    ]
    if request.user.is_superuser:
        context["options"] += [
            {"name": "Crear Cliente", "href": "/ordenes_servicio/crear_cliente/"},
            {"name": "Consultar Clientes", "href": "/ordenes_servicio/consultar_clientes/"}
        ]
        context["boxes"] = [
            {"title": "Clientes Registrados", "value": 0, "color": "bg-aqua", "icon": "ion-person-add"},
        ]
    if request.user.cargo == 'C':
        context["options"] += [
            {"name": "Crear Orden de Servicio", "href": "/ordenes_servicio/crear_orden_servicio/"},
            {"name": "Consultar Ordenes de Servicio", "href": "#"}
        ]
        context["boxes"] = [
            {"title": "Ordenes Registradas", "value": 0, "color": "bg-green", "icon": "ion-bag"},
        ]
    if request.user.cargo == 'O':
        context["options"] += [
            {"name": "Consultar Ordenes de Servicio", "href": "#"}
        ]
        context["boxes"] = [
            {"title": "Ordenes Por Atender", "value": 0, "color": "bg-yellow", "icon": "ion-folder"},
        ]

@login_required(login_url="/ordenes_servicio/login/")
def ordenes_welcome(request):
    context = {}
    manage_options(request,context)
    return render(request, "ordenes_servicio/index.html",context)


def gtfo(request):
    logout(request)
    return redirect("/ordenes_servicio/login/")

@login_required(login_url="/ordenes_servicio/login/")
def crear_orden_servicio(request):
    # user = request.user
    # Validar que el usuario sea un coordinador de servicios
    if True:
        form = None
        if request.method == 'POST':
            form = OrdenServicioForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Orden de servicio creada exitosamente')
                form = OrdenServicioForm()
            else:
                messages.error(request, 'El formulario NO es valido, Por favor corrige los errores')
                for error in form.errors:
                    messages.error(request, "Hay un problema con " + error)
        else:
            form = OrdenServicioForm()
            context = {"form":form}
            manage_options(request,context)
            return render(request, 'ordenes_servicio/crear_orden_servicio.html', context)
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')

def operadores_autocomplete(request):
    # user = request.user
    json = []
    if request.GET.get('q'):
        q = request.GET['q']
        criterio_uno = (models.Q(cedula__icontains=q) | models.Q(first_name__icontains=q) | models.Q(last_name__icontains=q))
        criterio_dos = models.Q(cargo="O") 
        data = User.objects.filter(criterio_uno & criterio_dos).values_list('cedula', 'first_name', 'last_name', 'id')[:10]
        arr = list(data)
        for tupla in arr:
            cedula = tupla[0]
            nombre = tupla[1]
            apellidos = tupla[2]
            id = tupla[3]
            json.append({'id': id, 'text':cedula + ' - ' + nombre + ' ' + apellidos})
    return JsonResponse(json, safe=False)

@login_required(login_url="/ordenes_servicio/login/")
def crear_cliente(request):
    if request.user.is_superuser:
        context = {"form": CrearClienteForm}
        manage_options(request,context)
        return render(request,"usuarios/crear_cliente.html",context)

@login_required(login_url="/ordenes_servicio/login/")
def consultar_clientes(request):
    if request.user.is_superuser:
        context = {"clientes": Cliente.objects.all()}
        manage_options(request,context)
        return render(request,"usuarios/consultar_clientes.html",context)