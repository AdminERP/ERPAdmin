from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PaymentAccountForm, ItemForm, ServiceOrderForm, CuentaCobroForm
from django.http import HttpResponse
from django.http import JsonResponse
from .models import CuentaPagar, Item, Payment, CuentaEmpresa
from .models import ServiceOrder, CuentaCobrar
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.core import serializers
from django.views.generic import CreateView
from django.core.mail import EmailMessage
#chartjs
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from apps.datosmaestros.models import DatoModel, ValorModel, CategoriaModel
from apps.ordenes_servicio.models import OrdenServicio
from decimal import Decimal
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Sum


def index(request):
	return render(request, 'cuentas/dashboard.html')

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Cobros"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35]]


# Crear cuenta por pagar
@permission_required('cuentas.add_cuentapagar', raise_exception=True)
def create_account (request):
	if request.POST:
		form = PaymentAccountForm(request.POST)
		# return HttpResponse(request)
		if form.is_valid():
			account = form.save()
			items = request.POST.get('allitems').split('~||~')
			for item in items:
				name,value = item.split('~|~')
				item = Item()
				item.name = name
				item.value = value
				item.account = account
				item.save()
			return redirect('listarPagar')
		else:
			return render(request, 'cuentas/crearCuenta.html', {'form':form})
	else:
		form = PaymentAccountForm()
		return render(request, 'cuentas/crearCuenta.html', {'form':form})

# Editar cuenta por pagar
@permission_required('cuentas.change_cuentapagar', raise_exception=True)
def payment_account_edit(request, pk):
	account = get_object_or_404(CuentaPagar, pk=pk)
	if account.status == '1' or account.status == '2':
		return redirect('listarPagar')
	items = account.item_set.all()
	form = PaymentAccountForm(request.POST or None, instance=account)
	if request.method == 'POST':
		if form.is_valid():
			account = form.save()
			items = request.POST.get('allitems').split('~||~')
			#delete items
			account.item_set.all().delete()
			#add items
			for item in items:
				name,value = item.split('~|~')
				item = Item()
				item.name = name
				item.value = value
				item.account = account
				item.save()
			return redirect('listarPagar')
		else:
			return render(request, 'cuentas/payment_account_edit.html', {'form':form})
	else:
		return render(request, 'cuentas/payment_account_edit.html', {'form':form, 'items':items})

# Pago de una cuenta
@permission_required('cuentas.add_payment', raise_exception=True)
def pay_account(request):
	if request.POST:
		# Cuentas bancarias en caso de error
		categoria = CategoriaModel.objects.get(nombre="Bancos")
		banks = DatoModel.objects.filter(categoria=categoria)

		account = get_object_or_404(CuentaPagar, pk=request.POST.get('account_id'))

		#si está paga
		if account.status == '2':
			cuentas = CuentaPagar.objects.all().order_by('id')
			return render(request, 'cuentas/listarCuentaPagar.html', {'cuentas':cuentas, 'error':'PAYD', 'order':account.order_id, 'banks':banks})
		# si está cancelada
		if account.status == '1':
			cuentas = CuentaPagar.objects.all().order_by('id')
			return render(request, 'cuentas/listarCuentaPagar.html', {'cuentas':cuentas, 'error':'CANCELLED', 'order':account.order_id, 'banks':banks})
		
		dato_id = request.POST.get('dato_id_bank')
		if int(dato_id) == 0:
			cuentas = CuentaPagar.objects.all().order_by('id')
			return render(request, 'cuentas/listarCuentaPagar.html', {'cuentas':cuentas, 'error':'NOBANK', 'order':account.order_id, 'banks':banks})
		try:
			bank = get_object_or_404(DatoModel, pk=dato_id)
			banks_values = ValorModel.objects.filter(dato_id=int(dato_id), nombre='saldo').first()
			saldo = Decimal(banks_values.valor)
			if saldo >= account.total:
				payment = Payment()
				payment.bank = bank
				payment.account = account
				payment.total = account.total
				saved = payment.save()
				saldo = saldo - payment.total
				banks_values.valor = saldo
				banks_values.save()
				account.status = '2'
				account.save()
			else:
				cuentas = CuentaPagar.objects.all().order_by('id')
				return render(request, 'cuentas/listarCuentaPagar.html', {'cuentas':cuentas, 'error':'NOCREDIT', 'order':account.order_id})
			return redirect('listarPagar')
		except (bank.DoesNotExist):
			pass
	else:
		return redirect('listarPagar')

# Pago de una cuenta
@permission_required('cuentas.change_cuentapagar', raise_exception=True)
def cancelle_account(request):
	if request.POST:
		account = get_object_or_404(CuentaPagar, pk=request.POST.get('account_id'))
		#si está paga
		if account.status == '2':
			cuentas = CuentaPagar.objects.all().order_by('id')
			return render(request, 'cuentas/listarCuentaPagar.html', {'cuentas':cuentas, 'error':'PAYD', 'order':account.order_id})
		# si está cancelada
		if account.status == '1':
			cuentas = CuentaPagar.objects.all().order_by('id')
			return render(request, 'cuentas/listarCuentaPagar.html', {'cuentas':cuentas, 'error':'CANCELLED', 'order':account.order_id})
		account.status = '1'
		account.save()
		return redirect('listarPagar')
	else:
		return redirect('listarPagar')

# Ver pagos
@permission_required('cuentas.view_payment', raise_exception=True)
def payments(request):
	payments = Payment.objects.all().order_by('id')
	return render(request, 'cuentas/payments.html', {'payments':payments})

#Ver detalles de una cuenta
@permission_required('cuentas.view_cuentapagar', raise_exception=True)
def payment_account_details(request, pk):
	account = get_object_or_404(CuentaPagar, pk=pk)
	items = account.item_set.all()
	payment = Payment.objects.filter(account_id=account.pk).first()
	if payment:
		return render(request, 'cuentas/payment_account_details.html', {'account':account, 'items':items, 'payment':payment})
	else:
		return render(request, 'cuentas/payment_account_details.html', {'account':account, 'items':items})

# Ver pagos
@permission_required('cuentas.view_payment', raise_exception=True)
def payment_details(request, pk):
	payment = get_object_or_404(Payment, pk=pk)
	return render(request, 'cuentas/payment_details.html', {'payment':payment})
	
def listarPagar (request):
	try:
		categoria = CategoriaModel.objects.get(nombre="Bancos")
	except CategoriaModel.DoesNotExist:
		categoria = None

	cuentas = CuentaPagar.objects.all().order_by('id')

	if categoria != None:
		banks = DatoModel.objects.filter(categoria=categoria)
	else:
		banks = None

	return render(request, 'cuentas/listarCuentaPagar.html', {'cuentas':cuentas, 'banks':banks})

@permission_required('cuentas.view_cuentascobrar', raise_exception=True)
def listarCobrar (request):
	cuentas = CuentaCobrar.objects.all().order_by('id')
	return render(request, 'cuentas/listarCuentaCobrar.html',{'cuentas':cuentas})

@permission_required("cuentas.view_ordenesservicio",raise_exception=True)
def listServiceOrder (request):
	orders = OrdenServicio.objects.all().order_by('id')
	form = CuentaCobroForm()
	return render(request, 'cuentas/listserviceorder.html', {'orders':orders,'form': form})

def listarDetalles (request):
	return render(request, 'cuentas/listarDetalles.html')

def createOrder(request):
	if request.POST:
		form = ServiceOrderForm(request.POST)
		if form.is_valid():
			order = form.save()
			return redirect('listServiceOrder')
		else:
			return render(request, 'cuentas/createOrder.html', {'form':form})
	else:
		form = ServiceOrderForm()
		return render(request, 'cuentas/createOrder.html', {'form': form})


@permission_required('cuentas.add_cuentascobrar', raise_exception=True)
def crearCuentaCobro(request,pk):
	if request.POST:
		form = CuentaCobroForm(request.POST)
		print(form)
		if form.is_valid():
			cuenta = form.save()
			order_id = cuenta.service_order_id
			serviceOrder = get_object_or_404(OrdenServicio, pk=order_id)
			user_id = serviceOrder.cliente_id;
			dato_id = cuenta.cuenta_empresa_id
			bank = get_object_or_404(DatoModel, pk=dato_id)
			banks_values = ValorModel.objects.filter(dato_id=int(dato_id), nombre='saldo').first()
			saldo = Decimal(banks_values.valor)
			correo = DatoModel.objects.get(id=user_id).valormodel_set.all().get(nombre='correo').valor
			body = render_to_string('cuentas/email_content.html', {
	                'servicio': cuenta.servicio,
	                'tarifa': cuenta.tarifa,
	                'costo': cuenta.costo_total,
	                'fecha_vencimiento':cuenta.fecha_vencimiento ,
	            	},
	        	)
			email_message = EmailMessage(subject='Mensaje de usuario',
				body=body,
				to=[correo],)
			email_message.content_subtype = 'html'
			email_message.send()
			OrdenServicio.objects.filter(pk=order_id).update(estado='CO')
			saldo = saldo + serviceOrder.valor
			banks_values.valor = saldo
			banks_values.save()
			return redirect('listarCobrar')
		else:
			return render(request, 'cuentas/listserviceorder.html', {'form':form})
	else:
		serviceOrder = get_object_or_404(OrdenServicio, pk=pk)
		form = CuentaCobroForm()
		return render(request, 'cuentas/crearCuentaCobrar.html', {'form': form, 'serviceOrder':serviceOrder})

@permission_required('cuentas.change_cuentascobrar', raise_exception=True)
def anularCuenta(request):
	print(request.POST)
	if request.POST:
		pk = request.POST.get('account_id')
		CuentaCobrar.objects.filter(pk=pk).update(estado=False)
		return redirect('listarCobrar')

def listarCuentaEmpresa (request):
	try:
		categoria = CategoriaModel.objects.get(nombre="Bancos")
	except CategoriaModel.DoesNotExist:
		categoria = None

	if categoria != None:
		banks = DatoModel.objects.filter(categoria=categoria)
	else:
		banks = None
	cuentas = CuentaEmpresa.objects.all().order_by('id')
	return render(request, 'cuentas/listarCuentasEmpresa.html',{'cuentas':cuentas, 'banks':banks})


# Graficas
def balances(request):
	ingresos = CuentaPagar.objects.filter(status='1').aggregate(Sum('total'))
	egresos = CuentaCobrar.objects.filter(estado=True).aggregate(Sum('costo_total'))
	return JsonResponse({'egresos':egresos, 'ingresos':ingresos})

