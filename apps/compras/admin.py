from django.contrib import admin

from .models import Articulo, Proveedor, SolicitudCompra, Cotizacion

# Register your models here.

admin.site.register(Articulo)
admin.site.register(Proveedor)
admin.site.register(SolicitudCompra)
admin.site.register(Cotizacion)