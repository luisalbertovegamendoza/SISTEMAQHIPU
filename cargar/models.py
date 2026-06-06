from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Empresa(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.nombre


class StockData(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    fecha = models.DateField()

    apertura = models.FloatField()

    cierre = models.FloatField()

    maximo = models.FloatField()

    minimo = models.FloatField()

    volumen = models.FloatField()

   
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        empresa = self.empresa.nombre if self.empresa else "Sin empresa"
        return f"{empresa} - {self.fecha}"