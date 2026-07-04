from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cargar.models import StockData



# =====================
# LANDING
# =====================
def index(request):

    # Si el usuario ya inició sesión
    if request.user.is_authenticated:
        return redirect('cargar_datos')

    return render(request, 'index.html')

# =====================
# LOGIN
# =====================

def login_usuario(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        # LOGIN CORRECTO
        if user is not None:

            login(request, user)

            messages.success(
                request,
                f"Bienvenido {user.username}"
            )

            # REDIRECCIONA A CARGAR
            return redirect('cargar_datos')

        # LOGIN INCORRECTO
        messages.error(
            request,
            "Usuario o contraseña incorrectos"
        )

        return redirect('index')

    return redirect('index')


# =====================
# REGISTRO
# =====================


def registro_usuario(request):

    print("ENTRO A REGISTRO")

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        print("first_name:", first_name)
        print("username:", username)
        print("email:", email)
        print("password1:", password1)
        print("password2:", password2)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name
        )

        print("USUARIO CREADO")

        return redirect('index')
# =====================
# LOGOUT
# =====================
def logout_usuario(request):
    logout(request)
    return redirect('index')


# =====================
# DASHBOARD (PROTEGIDO)
# =====================
@login_required
def dashboard(request):
    return render(request, 'dashboard/index.html')