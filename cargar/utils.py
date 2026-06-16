from cargar.models import StockData

def usuario_tiene_datos(usuario):
    return StockData.objects.filter(
        usuario=usuario
    ).exists()