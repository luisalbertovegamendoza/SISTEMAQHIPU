
from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [

    path(
        '',
        views.cargar_datos,
        name='cargar_datos'
    ),

     path(
        'descargar/',
        views.descargar_dataset_limpio,
        name='descargar_dataset_limpio'
    ),

]