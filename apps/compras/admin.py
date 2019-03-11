from django.contrib import admin

from .models import Articulo, Proveedor, SolicitudCompra

# Register your models here.

admin.site.register(Articulo)
admin.site.register(Proveedor)
admin.site.register(SolicitudCompra)
