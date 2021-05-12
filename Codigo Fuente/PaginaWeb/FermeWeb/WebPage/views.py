from django.shortcuts import render

# Import models
from .models import *

# Import Auth libraries
from django.contrib.auth import authenticate, logout, login as login_autent

# Add Decorators for Auth pages
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

# Logout View


# Login View


# Index
def index(request):
    #herramienta = sliderHerramienta.objects.all()
    #pintura = sliderPintura.objects.all()
    #material = sliderMateriales.objects.all()
    #return render(request, 'index.html', {'herramienta': herramienta, 'pintura': pintura, 'material': material})
    return render(request, 'index.html')

# Login
def login(request):
    #herramienta = sliderHerramienta.objects.all()
    #pintura = sliderPintura.objects.all()
    #material = sliderMateriales.objects.all()
    # Recibe un POST
    if request.POST:
        # Obtiene Datos
        usuario = request.POST.get("usuario")
        password = request.POST.get("clave")
        # Define usuario
        user = authenticate(request, username = usuario, password = password)
        # Verifica el usuario
        if user is not None and user.is_active:
            login_autent(request, user)
            #return render(request,'index.html', {'user': user, 'herramienta': herramienta, 'pintura': pintura, 'material': material})
            return render(request,'index.html')
        else:
            # Respuesta si no está
            ans = 1
            return render(request,'login.html', {'ans' : ans})
    return render(request,'login.html')

# Logout
def logoutView(request):
    logout(request)
    #herramienta = sliderHerramienta.objects.all()
    #pintura = sliderPintura.objects.all()
    #material = sliderMateriales.objects.all()
    #return render(request, 'index.html', {'herramienta': herramienta, 'pintura': pintura, 'material': material})
    return render(request,'index.html')

# SignUp
def signup(request):
    if request.POST:
        #Sliders
        herramienta = sliderHerramienta.objects.all()
        pintura = sliderPintura.objects.all()
        material = sliderMateriales.objects.all()
        rut = request.POST.get("txtRut")
        nombre = request.POST.get("txtNombre")
        apellidoPaterno = request.POST.get("txtApPaterno")
        apellidoMaterno = request.POST.get("txtApMaterno")
        correo = request.POST.get("txtCorreo")
        direccion = request.POST.get("txtDireccion")
        telefono = request.POST.get("txtNumero")
        usuario = request.POST.get("txtUsuario")
        clave1 = request.POST.get("clave1")
        clave2 = request.POST.get("clave2")
        try:
            user = User.objects.get(email = correo)
            ans = 3
            return render(request, 'formRegistro.html', {'ans' : ans})
        except:
            pass
        try:
            user = User.objects.get(username = usuario)         
            ans = 1
            return render(request,'formRegistro.html', {'ans' : ans})
        except:
            if clave1 != clave2:               
                ans = 2
                return render(request,'formRegistro.html', {'ans' : ans})
            user = User()
            user.first_name = nombre
            user.last_name = apellido
            user.email = correo
            user.username = usuario
            user.set_password(clave1)
            user.save()
            user = authenticate(request, username = usuario, password = clave1)
            login_autent(request, user)
            return render(request,'index.html', {'user' : user, 'herramienta': herramienta, 'pintura': pintura, 'material': material}) 
    return render(request,'formRegistro.html')

def ayuda(request):
    return render(request,'ayuda.html')

def misionyvision(request):
    return render(request,'misionyvision.html')

