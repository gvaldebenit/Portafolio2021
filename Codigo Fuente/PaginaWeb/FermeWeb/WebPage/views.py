from django.http.response import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

# Import models
from .models import *

# Import Auth libraries
from django.contrib.auth import authenticate, logout, login as login_autent

# Add Decorators for Auth pages
from django.contrib.auth.decorators import login_required, permission_required

#Add Detail View
from django.views.generic.detail import DetailView

# Add Generics
from django.views.generic import ListView, DetailView
from django.db.models import Q

from django.template.loader import render_to_string

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
        usuario = request.POST.get("txtUsuario")
        clave1 = request.POST.get("clave1")
        clave2 = request.POST.get("clave2")
        try:
            # Verifica que no exista el correo ya registrado
            user = User.objects.get(email = correo)
            ans = 3
            return render(request, 'registroCliente.html', {'ans' : ans})
        except:
            pass
        try:
            # Verifica que el username no exista
            user = User.objects.get(username = usuario)         
            ans = 1
            return render(request,'registroCliente.html', {'ans' : ans})
        except:
            # Verifica que las claves coincidan
            if clave1 != clave2:               
                ans = 2
                return render(request,'registroCliente.html', {'ans' : ans})
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
            cliente.idComuna = obj_comuna.idComuna
            cliente.idGrupo = user_group.pk 
            # Guardar Cliente
            cliente.save()
            user = authenticate(request, username = usuario, password = clave1)
            login_autent(request, user)
            return render(request,'index.html', {'user' : user}) 
    return render(request,'registroCliente.html')

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
        if fVenc == '':
            fVenc = None
            idProducto = f"{proveedor:03}" + f"{FamProd:03}" + f"00000000" + f"{TipoProd:03}" 
        else:    
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
        lista = Producto.objects.filter(idFamProducto__exact=3)          
        return lista

# Mision y Vision
def misionyvision(request):
    return render(request,'misionyvision.html')

# Contacto
def contacto(request):
    return render(request,'contacto.html')

#add-to-cart

def add_to_cart(request):
    #del request.session['cartdata']
    cart_p={}
    cart_p[str(request.GET['prodId'])]={
        'nombre':request.GET['nomProd'],
        'imagen':request.GET['imagen'],
        'cant':request.GET['cant'],
        'precio':request.GET['precio'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['prodId']) in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['prodId'])]['cant']=int(cart_p[str(request.GET['prodId'])]['cant'])
            cart_data.update(cart_data)
            request.session['cartdata']=cart_data
        else:
            cart_data=request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata']=cart_data
    else:
        request.session['cartdata']=cart_p
    
    return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

#carro
def cart_list(request):
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['cant']*int(item['precio']))
    return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})

#eliminar

def delete_cart_item(request):
    p_id=str(request.GET['prodId'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata']=cart_data
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['cant'])*int(item['precio'])
    t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

#actualizar

def update_cart_item(request):
    p_id=str(request.GET['prodId'])
    p_cant=request.GET['cant']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['prodId'])]['cant']=p_cant
            request.session['cartdata']=cart_data
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['cant'])*int(item['precio'])
    t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

