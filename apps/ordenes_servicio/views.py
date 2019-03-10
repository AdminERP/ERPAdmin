from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib import messages
from .forms import *
from django.db import models
from apps.usuarios.models import Cliente # ¿Modelo Cliente va en usuarios?
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
        {"name": "Inicio", "href": "/ordenes_servicio/welcome/"},
    ]
    if request.user.is_superuser:
        context["options"] += [
            {"name": "Django Admin Site", "href": "/admin"},
            {"name": "Crear Cliente", "href": "/ordenes_servicio/crear_cliente/"},
            {"name": "Consultar Clientes", "href": "/ordenes_servicio/consultar_clientes/"}
        ]
        context["boxes"] = [
            {"title": "Clientes Registrados", "value": 0, "color": "bg-aqua", "icon": "ion-person-add"},
        ]
    if request.user.cargo == 'C':
        context["options"] += [
            {"name": "Crear Orden de Servicio", "href": "/ordenes_servicio/crear_orden_servicio/"},
            {"name": "Consultar Ordenes de Servicio", "href": "/ordenes_servicio/consultar_orden_servicio/"}
        ]
        context["boxes"] = [
            {"title": "Ordenes Registradas", "value": 0, "color": "bg-green", "icon": "ion-bag"},
        ]
    if request.user.cargo == 'O':
        context["options"] += [
            {"name": "Consultar Ordenes de Servicio", "href": "/ordenes_servicio/consultar_orden_servicio/"}
        ]

        atender = len(OrdenServicio.objects.filter(estado="AS"))
        tramite = len(OrdenServicio.objects.filter(estado="TR"))
        context["boxes"] = [
            {"title": "Ordenes Por Atender", "value": atender, "color": "bg-yellow", "icon": "ion-folder"},
            {"title": "Ordenes en Tramite", "value": tramite, "color": "bg-red", "icon": "ion-clock"},
            {"title": "Ordenes Cerradas", "value": 0, "color": "bg-green-active", "icon": "ion-checkmark"},
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
        if request.method == 'POST':
            form = OrdenServicioForm(request.POST)
            if form.is_valid():
                form.instance.coordinador = request.user
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
        return redirect('/ordenes_servicio/')

@login_required(login_url="/ordenes_servicio/login/")
def aceptar_orden_servicio(request):
    if request.is_ajax():
        id = request.GET.get('orden_id', None)
        try:
            orden_servicio_aux = OrdenServicio.objects.get(id=id)
            usuario = request.user
            encargado = usuario.encargado_set.all().filter(id=id).count() == 1
            if usuario.cargo == "O" and encargado:
                orden_servicio_aux.estado = "TR"
                orden_servicio_aux.save()
                messages.success(request, 'Orden de Servicio Aceptada')
                return JsonResponse({'success': True})
            else:
                messages.error(request, 'No estas autorizado para realizar esta acción')
                return JsonResponse({'success': False})
        except:
            return JsonResponse({'orden_id': 0})


@login_required(login_url="/ordenes_servicio/login/")
def cerrar_orden_servicio(request):
    if request.is_ajax():
        id = request.GET.get('orden_id', None)
        try:
            orden_servicio_aux = OrdenServicio.objects.get(id=id)
            usuario = request.user
            encargado = usuario.encargado_set.all().filter(id=id).count() == 1
            if usuario.cargo == "O" and encargado:
                orden_servicio_aux.estado = "CE"
                orden_servicio_aux.save()
                messages.success(request, 'Orden de Servicio Cerrada')
                return JsonResponse({'success': True})
            else:
                messages.error(request, 'No estas autorizado para realizar esta acción')
                return JsonResponse({'success': False})
        except:
            return JsonResponse({'orden_id': 0})


@login_required(login_url="/ordenes_servicio/login/")
def consultar_orden_servicio(request):
    usuario = request.user
    if usuario.cargo == "C" or usuario.cargo == "O":
        context ={'ordenes': listar_ordenes(usuario)}
        manage_options(request,context)
        return render(request, 'ordenes_servicio/consultar_orden_servicio.html', context)
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('/ordenes_servicio/')

def listar_ordenes(usuario):
    return OrdenServicio.get_data(usuario)

def operadores_autocomplete(request):
    # user = request.user
    json = []
    if request.GET.get('q'):
        q = request.GET['q']
        criterio_uno = (models.Q(cedula__icontains=q) | models.Q(first_name__icontains=q) | models.Q(last_name__icontains=q))
        criterio_dos = models.Q(cargo="O") # Tiene que ser operario
        data = User.objects.filter(criterio_uno & criterio_dos).values_list('cedula', 'first_name', 'last_name', 'id')[:10]
        arr = list(data)
        for tupla in arr:
            cedula = tupla[0]
            nombre = tupla[1]
            apellidos = tupla[2]
            id = tupla[3]
            json.append({'id': id, 'text':cedula + ' - ' + nombre + ' ' + apellidos})
    return JsonResponse(json, safe=False, json_dumps_params={'ensure_ascii':False})

def clientes_autocomplete(request):
    # user = request.user
    json = []
    if request.GET.get('q'):
        q = request.GET['q']
        criterio_uno = (models.Q(nombres__icontains=q) | models.Q(apellidos__icontains=q) | models.Q(cedula__icontains=q) | models.Q(telefono__icontains=q) | models.Q(email__icontains=q))
        data = Cliente.objects.filter(criterio_uno).values_list('cedula', 'nombres', 'apellidos', 'id')[:10]
        arr = list(data)
        for tupla in arr:
            cedula = str(tupla[0])
            nombre = tupla[1]
            apellidos = tupla[2]
            id = tupla[3]
            json.append({'id': id, 'text':cedula + ' - ' + nombre + ' ' + apellidos})
    return JsonResponse(json, safe=False, json_dumps_params={'ensure_ascii':False})

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

@login_required(login_url="/ordenes_servicio/login/")
def cancelar_orden_servicio(request, id):
    try:
        orden_servicio_aux = OrdenServicio.objects.get(id=id)
    except:
        raise Http404
    print(request.user.encargado_set)
    pertenece_a_usuario =  request.user.encargado_set.all().filter(id=id).count() == 1
    if request.user.cargo == "C" or (request.user.cargo == "O" and pertenece_a_usuario):
        if request.method == 'POST':
            form = CancelarOrdenServicioForm(request.POST)
            if form.is_valid():
                orden_servicio_aux.comentarios = form.data["comentario_cancelar"]
                orden_servicio_aux.estado = "CA"
                orden_servicio_aux.save()
                messages.success(request, 'Orden Servicio Cancelada Exitosamente')
                return render(request, 'ordenes_servicio/consultar_orden_servicio.html',
                              {'ordenes': listar_ordenes(request.user)})
            else:
                messages.error(request, 'El formulario NO es valido, Por favor corrige los errores')
                for error in form.errors:
                    messages.error(request, "Hay un problema con " + error)
        if(orden_servicio_aux.estado == "CA"):
            messages.error(request, "No se puede cancelar una orden de servicio ya cancelada")
            return redirect('/ordenes_servicio/')
        elif(orden_servicio_aux.estado == "CE"):
            messages.error(request, "No se puede cancelar una orden de servicio cerrada")
            return redirect('/ordenes_servicio/')
        form = CancelarOrdenServicioForm()
        context = {"form":form}
        return render(request, 'ordenes_servicio/cancelar_orden_servicio.html', context)
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('/ordenes_servicio/')