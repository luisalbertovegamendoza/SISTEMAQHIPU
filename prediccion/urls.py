from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.prediccion_ia,
        name='prediccion'
    ),


    path(
        'descargar-excel/',
        views.descargar_prediccion_excel,
        name='descargar_prediccion_excel'
    ),

]


