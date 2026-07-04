
from django.db import models
from django.contrib.auth import get_user_model
from cargar.models import Empresa

User = get_user_model()

class Prediccion(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE
    )

    fecha_prediccion = models.DateField()

    precio_actual = models.FloatField()

    precio_predicho = models.FloatField()

    retorno = models.FloatField()

    senal = models.CharField(
        max_length=50
    )

    tendencia = models.CharField(
        max_length=50
    )

    interpretacion = models.TextField()

    riesgo = models.CharField(
        max_length=50
    )

    recomendacion = models.TextField()

    rsi = models.FloatField()

    estado_rsi = models.CharField(
        max_length=30
    )

    macd = models.FloatField()

    estado_macd = models.CharField(
        max_length=30
    )

    sma10 = models.FloatField()

    sma30 = models.FloatField()

    score_ia = models.FloatField()

    nivel_ia = models.CharField(
        max_length=50
    )

    mae = models.FloatField()

    rmse = models.FloatField()

    mape = models.FloatField()

    creado = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f"{self.empresa.nombre} - {self.fecha_prediccion}"
# Create your models here.
