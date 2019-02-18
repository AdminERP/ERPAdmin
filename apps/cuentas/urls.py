# Django

# Urls for the cuentas app

from django.urls import path
from apps.cuentas.views import *

urlpatterns = [
    path('', index, name='cuentas'),

    ]
