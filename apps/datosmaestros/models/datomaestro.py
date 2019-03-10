# Django
from django.db import models

TIPOS = (
    ('Relacionados', 'Relacionados'),
    ('Excluyentes', 'Excluyentes')
)

class DatoMaestroModel(models.Model):
    """
    DatoMaestroModel define un grupo de valores que
    pertenecen a determinada categoria.

    Un 'dato mestro' tiene uno o mas valores, los cuales
    pueden ser:
        - Reacionados: son valores que se relacionan entre si,
            es decir, un dato maestro une conceptos entre
            modulos del sistema ERP.
        - Excluyentes: son valores donde el dato maestro puede
            tomar uno de estos valores, es decir, un dato maestro
            puede tomar solo uno de las diferentes opciones (valores).
    """
    nombre = models.CharField(max_length = 20)
    descripcion = models.CharField(max_length = 200)
    tipo = models.CharField(max_length = 20, choices = TIPOS)
    estado = models.BooleanField(default = True)
    categoria = models.ForeignKey(
        'datosmaestros.CategoriaModel',
        on_delete = models.CASCADE
    )

    def __str__(self):
        return self.nombre
