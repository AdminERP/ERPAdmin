from django.shortcuts import render


# Create your views here.

def index (request):
	return render(request, 'cuentas/crearCuenta.html')

def listarPagar (request):
	return render(request, 'cuentas/listarCuentaPagar.html')

def listarCobrar (request):
	return render(request, 'cuentas/listarCuentaCobrar.html')

def listarDetalles (request):
	return render(request, 'cuentas/listarDetalles.html')
