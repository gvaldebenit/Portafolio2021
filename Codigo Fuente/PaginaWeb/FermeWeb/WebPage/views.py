from django.shortcuts import render

# Import models
from .models import *

# Import Auth libraries
from django.contrib.auth import authenticate, logout, login as login_autent

# Add Decorators for Auth pages
from django.contrib.auth.decorators import login_required, permission_required

#Add Detail View
from django.views.generic.detail import DetailView

# Add Generics
from django.views.generic import ListView
from django.db.models import Q

# Create your views here.

# Index
def index(request):
    return render(request, 'index.html')

# Login
def login(request):
    if request.POST:
        # Obtiene Datos
        usuario = request.POST.get("usuario")
        password = request.POST.get("clave")
        # Define usuario
        user = authenticate(request, username = usuario, password = password)
        # Verifica el usuario
        if user is not None and user.is_active:
            login_autent(request, user)
            return render(request,'index.html')
        else:
            # Respuesta si no está
            ans = 1
            return render(request,'login.html', {'ans' : ans})
    return render(request,'login.html')

# Logout
def logoutView(request):
    logout(request)
    return render(request,'index.html')

# SignUp
def signup(request):
    if request.POST:
        # Obtener los datos
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
            # Verifica que no exista el correo ya registrado
            user = User.objects.get(email = correo)
            ans = 3
            return render(request, 'formRegistro.html', {'ans' : ans})
        except:
            pass
        try:
            # Verifica que el username no exista
            user = User.objects.get(username = usuario)         
            ans = 1
            return render(request,'formRegistro.html', {'ans' : ans})
        except:
            # Verifica que las claves coincidan
            if clave1 != clave2:               
                ans = 2
                return render(request,'formRegistro.html', {'ans' : ans})
            # Crear un Usuario
            user = User()
            user.first_name = nombre
            user.last_name = apellidoPaterno
            user.email = correo
            user.username = correo
            user.set_password(clave1)
            # Guardar al Usuario
            user.save()
            # Crear un Cliente
            cliente = Cliente()
            cliente.rut = rut
            cliente.nombres = nombre
            cliente.apellidoPaterno = apellidoPaterno
            cliente.apellidoMaterno = apellidoMaterno
            cliente.email = correo
            cliente.telefono = telefono
            cliente.direccion = direccion
            # Guardar Cliente
            cliente.save()
            user = authenticate(request, username = usuario, password = clave1)
            login_autent(request, user)
            return render(request,'index.html', {'user' : user}) 
    return render(request,'formRegistro.html')

#Formulario Productos
def registroProducto(request):
    familiaPr = FamiliaProducto.objects.all()
    tipoPr = TipoProducto.objects.all()
    prov = Proveedor.objects.all()
    if request.POST:
        nombre = request.POST.get("txtNombre")
        precio = request.POST.get("txtPrecio")
        stock = request.POST.get("txtStock")
        stockCritico = request.POST.get("txtStockCritico")
        fVenc = request.POST.get("txtFvenn")
        proveedor = request.POST.get("txtProveedor")
        desc = request.POST.get("txtDescripcion")
        TipoProd = request.POST.get("TipoProducto")
        FamProd = request.POST.get("familiaProducto")
        obj_TipoProd = TipoProducto.objects.get(idTipoProducto=TipoProd)
        obj_TipoFam = FamiliaProducto.objects.get(idFamiliaProducto=FamProd)
        obj_Proveedor = Proveedor.objects.get(idProveedor=proveedor)
        idProducto = f"{proveedor:03}" + f"{FamProd:03}" + f"{fVenc:%d%m%Y}" + f"{TipoProd:03}" 

        prod = Producto(
            idProducto = idProducto,
            nombre = nombre,
            precio = precio,
            stock = stock,
            stockCrit = stockCritico,
            fVenc = fVenc,
            idTipoProducto = obj_TipoProd.idTipoProducto,
            idFamProducto = obj_TipoFam.idFamiliaProducto,
            idProveedor = obj_Proveedor.idProveedor,
            descripcion = desc
        )
        prod.save()
        return render(request,'registroProducto.html',{'familia_producto':familiaPr,'tipo_producto':tipoPr, 'proveedor':prov ,'mensaje':'Se grabo'})
    return render(request,'registroProducto.html',{'familia_producto':familiaPr,'tipo_producto':tipoPr})

# Busqueda
class ResultadosBusqueda(ListView):
    # Uso de Modelo
    model = Producto
    template_name = 'resultados.html'
    context_object_name = 'productos'

    def get_queryset(self): # Busqueda
        q = self.request.GET.get('q') 
        lista = Producto.objects.all()
        if q:
            lista = Producto.objects.filter(Q(nombre__icontains =q) | Q(descripcion__icontains=q))          
        return lista

def ayuda(request):
    return render(request,'ayuda.html')

def misionyvision(request):
    return render(request,'misionyvision.html')

def item(request,id):
    try:
        item = Producto.objects.get(id)
        return render(request,'item.html',{'item': item})
    except:
        item = Producto.objects.all()
        return render(request,'404.html')
    

#class Item(ListView):
#   model = Producto
#    template_name = 'item.html'

#     def get_queryset(self):
#        query = self.request.GET.get('q')
#        try: 
#            item = Producto.objects.filter(
#                Q(imagen__icontains=query) | Q(descripcion__icontains=query)
#            ).first()
#        except:
#            item = Producto.objects.all()
#        return item

class ItemDetail(DetailView):
    context_object_name = 'producto_detalle'
    model =  Producto
    template_name = 'item.html'