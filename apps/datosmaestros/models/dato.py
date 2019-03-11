# Django
from django.db import models

TIPOS = (
    ('Relacionados', 'Relacionados'),
    ('Excluyentes', 'Excluyentes')
)

class DatoModel(models.Model):
    """
    DatoModel define un grupo de valores que
    pertenecen a determinada categoria.

    Un 'dato' tiene uno o mas valores, los cuales
    pueden ser:
        - Reacionados: son valores que se relacionan entre si,
            es decir, un dato maestro que une conceptos entre
            modulos del sistema ERP.
        - Excluyentes: son valores donde el dato maestro puede
            tomar uno de estos valores, es decir, un dato maestro
            puede tomar solo uno de las diferentes opciones (valores).
    """
    nombre = models.CharField(max_length = 40)
    descripcion = models.CharField(max_length = 200)
    tipo = models.CharField(max_length = 20, choices = TIPOS)
    estado = models.BooleanField(default = True)
    categoria = models.ForeignKey(
        'datosmaestros.CategoriaModel',
        null = True,
        on_delete = models.CASCADE
    )

    def __str__(self):
        return self.nombre
