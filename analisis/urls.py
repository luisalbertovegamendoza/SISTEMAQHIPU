from django.urls import path
from .views import analisis_tecnico, descargar_analisis_excel


urlpatterns = [
   
     path(
        '',
        analisis_tecnico,
        name='analisis_tecnico'
    ),

    path(
        'descargar-excel/',
        descargar_analisis_excel,
        name='descargar_analisis_excel'
    ),



]