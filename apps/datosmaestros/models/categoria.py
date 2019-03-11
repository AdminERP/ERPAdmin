# Django
from django.db import models

class CategoriaModel(models.Model):
    """
    CategoriaModel define los diferentes tipos
    de datos maestros del sistema ERP, lo que
    permite agruparlos segun su función.

    Las 'categorias' son transversales a todo el
    sistema ERP permitiendo tener una unica
    'fuente de la verdad'.
    """
    nombre = models.CharField(max_length = 20, unique = True)
    descripcion = models.CharField(max_length = 200)
    estado = models.BooleanField(default = True)

    def __str__(self):
        return self.nombre
