from django.shortcuts import render

# Import models
from .models import *

# Import Auth libraries
from django.contrib.auth import authenticate, logout, login as login_autent

# Add Decorators for Auth pages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

# Add Generics
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q

# Date and DateTime Handler
from datetime import datetime

# Create your views here.

# Funcion para verificar si un usuario está en un grupo
def group_required(*group_names):

   def in_groups(u):
       if u.is_authenticated:
           if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
               return True
       return False
   return user_passes_test(in_groups)

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
    region = Region.objects.all()
    ciudad = Ciudad.objects.all()
    comuna = Comuna.objects.all() 
    if request.POST:
        # Obtener los datos
        rut = request.POST.get("txtRut")
        nombre = request.POST.get("txtNombre")
        apellidoPaterno = request.POST.get("txtApPaterno")
        apellidoMaterno = request.POST.get("txtApMaterno")
        correo = request.POST.get("txtCorreo")
        direccion = request.POST.get("txtDireccion")
        idcomuna = request.POST.get("comuna")
        obj_comuna = Comuna.objects.get(idComuna=idcomuna)
        telefono = request.POST.get("txtNumero")
        clave1 = request.POST.get("clave1")
        clave2 = request.POST.get("clave2")
        try:
            # Verifica que no exista el correo ya registrado
            user = User.objects.get(email = correo)
            ans = 3
            return render(request, 'registroCliente.html', {'ans' : ans, 'region':region, 'ciudad':ciudad, 'comuna':comuna})
        except:
            pass
        try:
            # Verifica que el username no exista
            user = User.objects.get(username = correo)         
            ans = 1
            return render(request,'registroCliente.html', {'ans' : ans, 'region':region, 'ciudad':ciudad, 'comuna':comuna})
        except:
            # Verifica que las claves coincidan
            if clave1 != clave2:               
                ans = 2
                return render(request,'registroCliente.html', {'ans' : ans, 'region':region, 'ciudad':ciudad, 'comuna':comuna})
            # Crear un Usuario
            user = User()
            user.first_name = nombre
            user.last_name = apellidoPaterno
            user.email = correo
            user.username = correo
            user.set_password(clave1)
            # Guardar al Usuario
            user.save()
            user_group = Group.objects.get(name="Cliente")
            user.groups.add(user_group)
            # Crear un Cliente
            cliente = Cliente()
            cliente.rut = rut
            cliente.nombres = nombre
            cliente.apellidoPaterno = apellidoPaterno
            cliente.apellidoMaterno = apellidoMaterno
            cliente.email = correo
            cliente.telefono = telefono
            cliente.direccion = direccion
            cliente.idComuna = obj_comuna
            cliente.idUsuario = user
            # Guardar Cliente
            cliente.save()
            user = authenticate(request, username = correo, password = clave1)
            login_autent(request, user)
            return render(request,'index.html', {'user' : user}) 
    return render(request,'registroCliente.html', {'region':region, 'ciudad':ciudad, 'comuna':comuna})

#Formulario Productos
# @login required(login_url='login/')
# @group_required('Vendedor', 'Empleado')
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
        if fVenc == '':
            fVenc = None
            idProducto = f"{proveedor:0>3}" + f"{FamProd:0>3}" + f"00000000" + f"{TipoProd:0>3}" 
        else:    
            fVenc = datetime.strptime(fVenc,"%Y-%m-%d")
            idProducto = f"{proveedor:0>3}" + f"{FamProd:0>3}" + fVenc.strftime("%d%m%Y") + f"{TipoProd:0>3}" 
        prod = Producto(
            idProducto = idProducto,
            nombre = nombre,
            precio = precio,
            stock = stock,
            stockCrit = stockCritico,
            fVenc = fVenc,
            idTipoProducto = obj_TipoProd,
            idFamProducto = obj_TipoFam,
            idProveedor = obj_Proveedor,
            descripcion = desc
        )
        prod.save()
        return render(request,'registroProducto.html',{'familia_producto':familiaPr,'tipo_producto':tipoPr, 'proveedor':prov ,'mensaje':'Producto Registrado'})
    return render(request,'registroProducto.html',{'familia_producto':familiaPr,'tipo_producto':tipoPr, 'proveedor':prov})

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

# Item
class ItemDetail(DetailView):
    context_object_name = 'producto_detalle'
    model =  Producto
    template_name = 'item.html'

# Ayuda
def ayuda(request):
    return render(request,'ayuda.html')

# Pagina Pinturas
class ListaPinturas(ListView):
    # Uso de Modelo
    model = Producto
    template_name = 'resultados.html'
    context_object_name = 'productos'

    def get_queryset(self): # Busqueda
        lista = Producto.objects.filter(idFamProducto__exact=1)         
        return lista

# Pagina Herramientas
class ListaHerramienta(ListView):
    # Uso de Modelo
    model = Producto
    template_name = 'resultados.html'
    context_object_name = 'productos'

    def get_queryset(self): # Busqueda
        lista = Producto.objects.filter(idFamProducto__exact=2)          
        return lista

# Pagina Materiales
class ListaMateriales(ListView):
    # Uso de Modelo
    model = Producto
    template_name = 'resultados.html'
    context_object_name = 'productos'

    def get_queryset(self): # Busqueda
        user = self.request.user
        if user.groups.filter(name = "Proveedor").exists():

            lista = Producto.objects.filter(idFamProducto__exact=3)          
        return lista

# Mision y Vision
def misionyvision(request):
    return render(request,'misionyvision.html')

# Contacto
def contacto(request):
    return render(request,'contacto.html')

# Orden Compra
# @login required(login_url='login/')
# @group_required('Empleado')
def encargarProducto(request):
    #pass
    return render(request, 'registroOrden.html')

# Listado Orden Compra
# @login required(login_url='login/')
# @group_required('Empleado', 'Proveedor')
class ListaOrdenCompra(ListView):
    # Uso de Modelo
    model = OrdenCompra
    template_name = 'ListadoOrden.html'
    context_object_name = 'Ordenes de Compra'

    def get_queryset(self): # Busqueda
        user = self.request.user
        if user.groups.filter(name__in="Proveedor").exists():
            try:
                proveedor = Proveedor.objects.first(idUsuario=user)
                lista = OrdenCompra.objects.filter(idProducto__idProveedor = proveedor)          
                return lista
            except:
                lista = []
                return lista
        else:
            lista = OrdenCompra.objects.all()
            return lista

# Listado Orden Compra
# @login required(login_url='login/')
# @group_required('Empleado', 'Vendedor')
def crearProveedor(request):
    region = Region.objects.all()
    ciudad = Ciudad.objects.all()
    comuna = Comuna.objects.all() 
    rubro = Rubro.objects.all()
    if request.POST:
        # Obtener los datos
        rut = request.POST.get("txtRut")
        nombre = request.POST.get("txtNombre")
        correo = request.POST.get("txtCorreo")
        direccion = request.POST.get("txtDireccion")
        idcomuna = request.POST.get("comuna")
        obj_comuna = Comuna.objects.get(idComuna=idcomuna)
        telefono = request.POST.get("txtNumero")
        representante = request.POST.get("txtRepresentante")
        rubro = request.POST.get("rubro")
        obj_rubro = Rubro.objects.get(idRubro=rubro)
        clave1 = request.POST.get("clave1")
        clave2 = request.POST.get("clave2")
        try:
            # Verifica que no exista el correo ya registrado
            user = User.objects.get(email = correo)
            ans = 3
            return render(request, 'registroProveedor.html', {'ans' : ans, 'region':region, 'ciudad':ciudad, 'comuna':comuna, 'rubro':rubro})
        except:
            pass
        try:
            # Verifica que el username no exista
            user = User.objects.get(username = correo)         
            ans = 1
            return render(request,'registroProveedor.html', {'ans' : ans, 'region':region, 'ciudad':ciudad, 'comuna':comuna, 'rubro':rubro})
        except:
            # Verifica que las claves coincidan
            if clave1 != clave2:               
                ans = 2
                return render(request,'registroProveedor.html', {'ans' : ans, 'region':region, 'ciudad':ciudad, 'comuna':comuna, 'rubro':rubro})
            # Crear un Usuario
            user = User()
            user.first_name = nombre
            user.last_name = ''
            user.email = correo
            user.username = correo
            user.set_password(clave1)
            # Guardar al Usuario
            user.save()
            user_group = Group.objects.get(name="Proveedor")
            user.groups.add(user_group)
            # Crear un Proveedor
            proveedor = Proveedor()
            proveedor.rut = rut
            proveedor.nombres = nombre
            proveedor.apellidoPaterno = ''
            proveedor.apellidoMaterno = ''
            proveedor.telefono = telefono
            proveedor.direccion = direccion
            proveedor.idComuna = obj_comuna
            proveedor.idUsuario = user
            proveedor.representante = representante
            proveedor.idRubro = obj_rubro
            # Guardar Proveedor
            proveedor.save()
            msg = 'Proveedor Creado Exitosamente' # Mensaje de Exito
            return render(request,'registroProveedor', {'region':region, 'ciudad':ciudad, 'comuna':comuna, 'rubro':rubro, 'msg': msg}) 
    return render(request,'registroProveedor.html', {'region':region, 'ciudad':ciudad, 'comuna':comuna, 'rubro':rubro})

