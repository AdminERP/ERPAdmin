from django.shortcuts import render, redirect, get_object_or_404
from .forms import PaymentAccountForm, ItemForm, ServiceOrderForm
from django.http import HttpResponse
from django.http import JsonResponse
from .models import CuentaPagar, Item, Payment, CuentaEmpresa
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.core import serializers
from django.views.generic import CreateView


# Create your views here.
def index (request):
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
	return render(request, 'cuentas/listarCuentaCobrar.html')

def listarDetalles (request):
	return render(request, 'cuentas/listarDetalles.html')

def createOrder(request):
    form = ServiceOrderForm()
    return render(request, 'cuentas/createOrder.html', {'form': form})