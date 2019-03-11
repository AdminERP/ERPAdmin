# Django
from django.db import models

class ValorModel(models.Model):
    """
    ValorModel define un valor relacionado a un
    determinado dato maestro, sea relacionado o excluyente.
    """
    nombre = models.CharField(max_length = 40)
    descripcion = models.CharField(max_length = 200)
    valor = models.CharField(max_length = 40)
    estado = models.BooleanField(default = True)
    dato = models.ForeignKey(
        'datosmaestros.DatoModel',
        null = True,
        on_delete = models.CASCADE
    )

    def __str__(self):
        return self.nombre
