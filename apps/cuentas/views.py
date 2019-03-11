from django.shortcuts import render, redirect, get_object_or_404
from .forms import PaymentAccountForm, ItemForm, ServiceOrderForm, CuentaCobroForm
from django.http import HttpResponse
from django.http import JsonResponse
from .models import CuentaPagar, Item, Payment, CuentaEmpresa
from .models import ServiceOrder, CuentaCobrar
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.core import serializers
from django.views.generic import CreateView
#chartjs
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView


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


# Create your views here.
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

def pay_account(request):
	if request.POST:
		bank = get_object_or_404(CuentaEmpresa, pk=1)
		account = get_object_or_404(CuentaPagar, pk=request.POST.get('account_id'))
		#si está paga
		if account.status == '2':
			cuentas = CuentaPagar.objects.all().order_by('id')
			return render(request, 'cuentas/listarCuentaPagar.html', {'cuentas':cuentas, 'error':'PAYD', 'order':account.order_id})
		# si está cancelada
		if account.status == '1':
			cuentas = CuentaPagar.objects.all().order_by('id')
			return render(request, 'cuentas/listarCuentaPagar.html', {'cuentas':cuentas, 'error':'CANCELLED', 'order':account.order_id})
		if bank.saldo >= account.total:
			payment = Payment()
			payment.bank = bank
			payment.account = account
			payment.total = account.total
			saved = payment.save()
			bank.saldo = bank.saldo - payment.total
			bank.save()
			account.status = '2'
			account.save()
		else:
			cuentas = CuentaPagar.objects.all().order_by('id')
			return render(request, 'cuentas/listarCuentaPagar.html', {'cuentas':cuentas, 'error':'NOCREDIT', 'order':account.order_id})
		return redirect('listarPagar')
	else:
		return redirect('listarPagar')

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

def payments(request):
	payments = Payment.objects.all().order_by('id')
	return render(request, 'cuentas/payments.html', {'payments':payments})

def payment_account_details(request, pk):
	account = get_object_or_404(CuentaPagar, pk=pk)
	items = account.item_set.all()
	payment = Payment.objects.filter(account_id=account.pk).first()
	if payment:
		return render(request, 'cuentas/payment_account_details.html', {'account':account, 'items':items, 'payment':payment})
	else:
		return render(request, 'cuentas/payment_account_details.html', {'account':account, 'items':items})

def payment_details(request, pk):
	payment = get_object_or_404(Payment, pk=pk)
	return render(request, 'cuentas/payment_details.html', {'payment':payment})
	
def listarPagar (request):
	cuentas = CuentaPagar.objects.all().order_by('id')
	return render(request, 'cuentas/listarCuentaPagar.html', {'cuentas':cuentas})

def listarCobrar (request):
	cuentas = CuentaCobrar.objects.all().order_by('id')
	return render(request, 'cuentas/listarCuentaCobrar.html',{'cuentas':cuentas})

def listServiceOrder (request):
	orders = ServiceOrder.objects.all().order_by('id')
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

def crearCuentaCobro(request,pk):
	if request.POST:
		form = CuentaCobroForm(request.POST)
		print(form)
		if form.is_valid():
			cuenta = form.save()
			return redirect('listarCobrar')
		else:
			return render(request, 'cuentas/listserviceorder.html', {'form':form})
	else:
		serviceOrder = get_object_or_404(ServiceOrder, pk=pk) 
		form = CuentaCobroForm()
		return render(request, 'cuentas/crearCuentaCobrar.html', {'form': form, 'serviceOrder':serviceOrder})

def anularCuenta(request):
	print(request.POST)
	if request.POST:
		pk = request.POST.get('account_id')
		CuentaCobrar.objects.filter(pk=pk).update(estado=False)
		return redirect('listarCobrar')
def listarCuentaEmpresa (request):
	cuentas = CuentaEmpresa.objects.all().order_by('id')
	return render(request, 'cuentas/listarCuentasEmpresa.html',{'cuentas':cuentas})