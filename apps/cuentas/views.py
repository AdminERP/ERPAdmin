from django.shortcuts import render
from .forms import PaymentAccountForm, ItemForm, ServiceOrderForm
from django.http import HttpResponse
from .models import Item
from django_datatables_view.base_datatable_view import BaseDatatableView
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
				item.account_id = account.id
				item.save()
			return render(request, 'cuentas/crearCuenta.html')
		else:
			return render(request, 'cuentas/crearCuenta.html', {'form':form})
	else:
		form = PaymentAccountForm()
		return render(request, 'cuentas/crearCuenta.html', {'form':form})

def listarPagar (request):
	return render(request, 'cuentas/listarCuentaPagar.html')

def listarCobrar (request):
	return render(request, 'cuentas/listarCuentaCobrar.html')

def listarDetalles (request):
	return render(request, 'cuentas/listarDetalles.html')

def createOrder(request):
    form = ServiceOrderForm()
    return render(request, 'cuentas/createOrder.html', {'form': form})