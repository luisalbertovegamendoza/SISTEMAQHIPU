
from django.urls import path
from . import views



urlpatterns = [
   path(
        '',
        views.prediccion_ia,
        name='prediccion'
    ),

   

]


