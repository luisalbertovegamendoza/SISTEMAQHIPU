from django.urls import path
from .views import analisis_tecnico



urlpatterns = [
   
     path(
        '',
        analisis_tecnico,
        name='analisis_tecnico'
    ),
   

]