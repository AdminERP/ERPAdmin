# Django

# Urls for the cuentas app

from django.urls import path
from apps.cuentas.views import *

urlpatterns = [
    path('', index, name='crearCuenta'),
    path('listarPagar/', listarPagar,  name='listarPagar'),
    path('listarCobrar/', listarCobrar, name='listarCobrar'),
    path('detalles/', listarDetalles, name='detalles'),
    path('payment_account_edit/<pk>', payment_account_edit, name='payment_account_edit'),
    path('payment_account_details/<pk>', payment_account_details, name='payment_account_details'),
    path('pay_account/', pay_account, name='pay_account'),
    path('payments/', payments, name='payments'),
    path('payment_details/<pk>', payment_details, name='payment_details'),
    path('createOrder/', createOrder, name='createOrder'),
]
