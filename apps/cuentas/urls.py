# Django

# Urls for the cuentas app

from django.urls import path
from apps.cuentas.views import *

urlpatterns = [
    #path('', index, name='crearCuenta'),
    path('', index, name='index'),
    path('create_account', create_account, name='crearCuenta'),
    path('listarPagar/', listarPagar,  name='listarPagar'),
    path('listarCobrar/', listarCobrar, name='listarCobrar'),
    path('detalles/', listarDetalles, name='detalles'),
    path('payment_account_edit/<pk>', payment_account_edit, name='payment_account_edit'),
    path('payment_account_details/<pk>', payment_account_details, name='payment_account_details'),
    path('pay_account/', pay_account, name='pay_account'),
    path('cancelle_account/', cancelle_account, name='cancelle_account'),
    path('payments/', payments, name='payments'),
    path('payment_details/<pk>', payment_details, name='payment_details'),
    path('createOrder/', createOrder, name='createOrder'),
    path('listOrders/', listServiceOrder, name='listServiceOrder'),
    path('crearCuentaCobro/<pk>', crearCuentaCobro, name='crearCuentaCobro'),
    path('anularCuenta/', anularCuenta, name='anularCuenta'),
    path('listarCuentaEmpresa/', listarCuentaEmpresa, name='listarCuentaEmpresa'),
    path('dashboard_graph_1/', LineChartJSONView.as_view(), name='dashboard_graph_1'),
    path('balances/', balances, name='balances'),
]
