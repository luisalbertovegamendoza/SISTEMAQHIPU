

from django.contrib import admin #panel administrador
from django.urls import path , include  # conecta apps
#from home.views import IndexView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('cargar/', include('cargar.urls')),
    path('prediccion/', include('prediccion.urls')),
    path('dashboard/', include('dashborad.urls')),
    path('analisis/', include('analisis.urls')),

     # USUARIOS
    path('login/', views.login_usuario , name='login'),
    path('logout/', views.logout_usuario,name='logout'),
    path('registro/', views.registro_usuario, name='registro'),



    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
