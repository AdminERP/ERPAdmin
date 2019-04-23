from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from apps.datosmaestros.models.dato import DatoModel
from apps.datosmaestros.models.categoria import CategoriaModel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission

#autocomplete
from apps.usuarios.models import *
from apps.usuarios.forms import *
from django.http import JsonResponse

def to_welcome(request):
    return redirect('/ordenes_servicio/welcome')

def manage_options(request, context):
    ###############################################################################################     PERMISOS
    ###############################################################################################
    if request.user.has_perm('ordenes_servicio.add_ordenservicio'):
        ordenes = OrdenServicio.objects.filter(coordinador=request.user).order_by('-id')
        context["ordenes_timeline"] = ordenes

        registradas = ordenes.count()
        tramite = ordenes.filter(estado="TR").count()
        cerradas = ordenes.filter(estado="CE").count()
        canceladas = ordenes.filter(estado="CA").count()
        context["boxes"] = [
            {"title": "Ordenes Registradas", "value": registradas, "color": "bg-purple", "icon": "ion-clipboard"},
            {"title": "Ordenes en Trámite", "value": tramite, "color": "bg-light-blue-active", "icon": "ion-android-sync"},
            {"title": "Ordenes Cerradas", "value": cerradas, "color": "bg-green-active", "icon": "ion-checkmark"},
            {"title": "Ordenes Canceladas", "value": canceladas, "color": "bg-red-active", "icon": "ion-close"},
        ]

    if request.user.has_perm('ordenes_servicio.execute_ordenservicio'):
        ordenes = OrdenServicio.objects.filter(encargado=request.user).order_by('-id')
        context["ordenes_timeline"] = ordenes

        atender = ordenes.filter(estado="AS").count()
        tramite = ordenes.filter(estado="TR").count()
        cerradas = ordenes.filter(estado="CE").count()
        canceladas = ordenes.filter(estado="CA").count()

        context["boxes"] = [
            {"title": "Ordenes Por Atender", "value": atender, "color": "bg-teal-active", "icon": "ion-folder"},
            {"title": "Ordenes en Trámite", "value": tramite, "color": "bg-light-blue-active", "icon": "ion-android-sync"},
            {"title": "Ordenes Cerradas", "value": cerradas, "color": "bg-green-active", "icon": "ion-checkmark"},
            {"title": "Ordenes Canceladas", "value": canceladas, "color": "bg-red-active", "icon": "ion-close"},
        ]

    ###############################################################################################
    ###############################################################################################
    if not request.user.is_anonymous:
        context["cargo"] = request.user.cargo

@login_required(login_url='/')
@permission_required(("ordenes_servicio.view_ordenservicio"), raise_exception=True, login_url='/')
def ordenes_welcome(request):
    context = {}
    manage_options(request,context)
    return render(request, "ordenes_servicio/index.html",context)

def gtfo(request):
    logout(request)
    return redirect("/")

@permission_required('ordenes_servicio.add_ordenservicio', raise_exception=True)
def crear_orden_servicio(request):
    if request.method == 'POST':
        form = OrdenServicioForm(request.POST)
        if form.is_valid():
            form.instance.coordinador = request.user
            form.instance.valor = int(form.instance.servicio_vendido.valormodel_set.all().get(nombre="valor").valor)
            form.save()
            messages.success(request, 'Orden de servicio creada exitosamente')
            return redirect('/ordenes_servicio/consultar_orden_servicio')
        else:
            messages.error(request, 'El formulario NO es valido, Por favor corrige los errores')
            for error in form.errors:
                messages.error(request, "Hay un problema con " + error)
    else:
        form = OrdenServicioForm()

    context = {"form": form}
    manage_options(request, context)
    return render(request, 'ordenes_servicio/crear_orden_servicio.html', context)

@permission_required("ordenes_servicio.execute_ordenservicio", raise_exception=True)
def aceptar_orden_servicio(request):
    if request.is_ajax():
        id = request.GET.get('orden_id', None)
        try:
            orden_servicio_aux = OrdenServicio.objects.get(id=id)
            usuario = request.user
            encargado = usuario.encargado_set.all().filter(id=id).count() == 1
            if encargado:
                orden_servicio_aux.estado = "TR"
                orden_servicio_aux.save()
                messages.success(request, 'Orden de Servicio Aceptada')
                return JsonResponse({'success': True})
            else:
                messages.error(request, 'No eres el asignado para esta orden de servicio')
                return JsonResponse({'success': False})
        except:
            return JsonResponse({'orden_id': 0})


@permission_required("ordenes_servicio.execute_ordenservicio", raise_exception=True)
def cerrar_orden_servicio(request):
    if request.is_ajax():
        id = request.GET.get('orden_id', None)
        try:
            orden_servicio_aux = OrdenServicio.objects.get(id=id)
            usuario = request.user
            encargado = usuario.encargado_set.all().filter(id=id).count() == 1
            if encargado:
                orden_servicio_aux.estado = "CE"
                orden_servicio_aux.save()
                messages.success(request, 'Orden de Servicio Cerrada')
                return JsonResponse({'success': True})
            else:
                messages.error(request, 'No estas autorizado para realizar esta acción')
                return JsonResponse({'success': False})
        except:
            return JsonResponse({'orden_id': 0})


@permission_required(perm=("ordenes_servicio.execute_ordenservicio",
                           "ordenes_servicio.cancel_ordenservicio"),
                     raise_exception=True)
def cancelar_orden_servicio(request):
    if request.is_ajax():
        id = request.GET.get('orden_id', None)
        comentarios = request.GET.get('comentarios', None)
        try:
            orden_servicio_aux = OrdenServicio.objects.get(id=id)
        except:
            return JsonResponse({'success': False})
        pertenece_a_usuario =  request.user.encargado_set.all().filter(id=id).count() == 1
        if pertenece_a_usuario:
            error = False
            if(orden_servicio_aux.estado == "CA"):
                messages.error(request, "No se puede cancelar una orden de servicio ya cancelada")
                error = True
            elif(orden_servicio_aux.estado == "CE"):
                messages.error(request, "No se puede cancelar una orden de servicio cerrada")
                error = True
            if comentarios != "":
                orden_servicio_aux.comentarios = comentarios
                orden_servicio_aux.estado = "CA"
                orden_servicio_aux.save()
                messages.success(request, 'Orden de Servicio Cancelada Exitósamente')
                return JsonResponse({'success': True})
            else:
                error = True
                messages.error(request, 'Debe agregar un comentarios de cancelacion')
            if error:
                return JsonResponse({'success': False})
        else:
            messages.error(request, 'No estas autorizado para realizar esta acción')
            return JsonResponse({'success': False})

@permission_required("ordenes_servicio.view_ordenservicio",raise_exception=True)
def consultar_orden_servicio(request):
    usuario = request.user
    if usuario.has_perm('ordenes_servicio.view_ordenservicio'):
        context ={'ordenes': OrdenServicio.get_data(usuario)}
        manage_options(request,context)
        return render(request, 'ordenes_servicio/consultar_orden_servicio.html', context)
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('/ordenes_servicio/')

def operadores_autocomplete(request):
    # user = request.user
    json = []
    if request.GET.get('q'):
        q = request.GET['q']
        criterio_uno = (models.Q(cedula__icontains=q) | models.Q(first_name__icontains=q) | models.Q(last_name__icontains=q))
        perm = Permission.objects.get(codename='execute_ordenservicio')
        criterio_dos = models.Q(cargo__permissions=perm)
        data = Usuario.objects.filter((criterio_uno & criterio_dos) | (criterio_uno & models.Q(is_superuser=True))).values_list('cedula', 'first_name', 'last_name', 'id')[:10]
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
        categoria = CategoriaModel.objects.get(nombre = 'clientes')
        clientes_query = DatoModel.objects.filter(categoria = categoria.id).distinct()
        data =clientes_query.filter(valormodel__valor__icontains=q).values_list('id')[:10]
        arr = list(data)
        for tupla in arr:
            id = tupla[0]
            cedula = DatoModel.objects.get(id=id).valormodel_set.all().get(nombre="cedula").valor
            nombres = DatoModel.objects.get(id=id).valormodel_set.all().get(nombre="nombres").valor
            apellidos = DatoModel.objects.get(id=id).valormodel_set.all().get(nombre="apellidos").valor
            json.append({'id': id, 'text':cedula + ' - ' + nombres + ' ' + apellidos})
    return JsonResponse(json, safe=False, json_dumps_params={'ensure_ascii':False})

'''
#### DATOS MAESTROS
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
'''
