from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

# Import models
from .models import *

# Import Auth libraries
from django.contrib.auth import authenticate, logout, login as login_autent

# Add Decorators for Auth pages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

# Add Generics
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q, F

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
            mensaje = 'Usuario Inexistente. Pruebe con otros Datos'
            return render(request,'login.html', {'mensaje' : mensaje})
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
            mensaje = 'Email ya existente en la base de datos'
            return render(request, 'registroCliente.html', {'mensaje' : mensaje, 'region':region, 'ciudad':ciudad, 'comuna':comuna})
        except:
            pass
        try:
            # Verifica que el username no exista
            user = User.objects.get(username = correo)         
            mensaje = 'Usuario ya Existente'
            return render(request,'registroCliente.html', {'mensaje' : mensaje, 'region':region, 'ciudad':ciudad, 'comuna':comuna})
        except:
            # Verifica que las claves coincidan
            if clave1 != clave2:               
                mensaje = 'Las contraseñas no coinciden'
                return render(request,'registroCliente.html', {'mensaje' : mensaje, 'region':region, 'ciudad':ciudad, 'comuna':comuna})
            # Crear un Usuario
            try:
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
            except:
                mensaje = 'Error al crear Usuario'
                return render(request,'registroCliente.html', {'mensaje' : mensaje, 'region':region, 'ciudad':ciudad, 'comuna':comuna})
    return render(request,'registroCliente.html', {'region':region, 'ciudad':ciudad, 'comuna':comuna})

#Formulario Productos
@login_required(login_url='login/')
@group_required('Vendedor', 'Empleado')
def registroProducto(request):
    familiaPr = FamiliaProducto.objects.all()
    tipoPr = TipoProducto.objects.all()
    prov = Proveedor.objects.all()
    if request.POST:
        try:
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
            mensaje = 'Producto Registrado'
            return render(request,'registroProducto.html',{'familia_producto':familiaPr,'tipo_producto':tipoPr, 'proveedor':prov ,'mensaje': mensaje})
        except:
            mensaje = 'Error al Registrar Producto'   
            return render(request,'registroProducto.html',{'familia_producto':familiaPr,'tipo_producto':tipoPr, 'proveedor':prov ,'mensaje': mensaje})
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

# Orden Compra
@login_required(login_url='login/')
@group_required('Empleado')
def encargarProducto(request, id_prod=None):
    productos = Producto.objects.all()
    prov = Proveedor.objects.all()
    if id_prod is not None: # Verifica si Trae un Producto como parametro
        item = Producto.objects.get(pk=id_prod) # Traer el item y darlo a la pagina
        return render(request,'registroOrdenCompra.html',{'proveedor':prov, 'productos':productos , 'item': item})
    if request.POST: # Generar una Orden de Compra
        try:
            # Recoger los Datos
            producto = request.POST.get("txtProducto")
            cantidad = request.POST.get("txtCantidad")
            total = request.POST.get('txtTotal')        
            comentario = request.POST.get("txtDescripcion")
            fechaPedido = datetime.now()
            user = request.user        
            obj_Producto = Producto.objects.get(idProducto=producto)
            empleado = Empleado.objects.first(idUsuario=user)
            if request.POST['submit'] == 'Enviar': # Se presiona el Btn Enviar
                enviado = True
            elif request.POST['submit'] == 'Guardar': # Se presionael Btn Guardar
                enviado = False
            else:
                enviado = False
            # Generar la Orden de Compra
            orden = OrdenCompra(
                idProducto = obj_Producto,
                cantidad = cantidad,
                total = total,
                comentario = comentario,
                fechaPedido = fechaPedido,
                idEmpleado = empleado,
                enviada = enviado
            )
            orden.save()
            if enviado == True:
                mensaje = 'Orden Registrada y Enviada'
            else:
                mensaje = 'Orden Registrada'
            return render(request,'registroOrdenCompra.html',{'proveedor':prov, 'productos':productos ,'mensaje': mensaje})
        except:
            mensaje = 'Error al intentar registrar'
            return render(request,'registroOrdenCompra.html',{'proveedor':prov, 'productos':productos ,'mensaje': mensaje})
    return render(request,'registroOrdenCompra.html',{'proveedor':prov, 'productos':productos})

# Listado Orden Compra
@login_required(login_url='login/')
@group_required('Empleado', 'Proveedor')
class ListaOrdenCompra(ListView):
    # Uso de Modelo
    model = OrdenCompra
    template_name = 'listadoOrden.html'
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
    
    def get_context_data(self, *args, **kwargs): # Context Data de Productos con Stock menor al Stock Critico
        context = super(ListaOrdenCompra, self).get_context_data(*args, **kwargs)
        context['Productos_StockCrit'] = Producto.objects.filter(stock__lte = F('stockCrit')) #Query
        return context 

# Detalle Orden Compra
@login_required(login_url='login/')
@group_required('Empleado', 'Proveedor')
class OrdenCompraDetail(DetailView):
    context_object_name = 'OrdenCompra_detalle'
    model =  OrdenCompra
    template_name = 'ordenDetail.html'

# Crear Proveedor
@login_required(login_url='login/')
@group_required('Empleado', 'Vendedor')
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
            mensaje = 'Email ya existente en la base de datos'
            return render(request, 'registroProveedor.html', {'mensaje' : mensaje, 'region':region, 'ciudad':ciudad, 'comuna':comuna, 'rubro':rubro})
        except:
            pass
        try:
            # Verifica que el username no exista
            user = User.objects.get(username = correo)         
            mensaje = 'Usuario ya Existente'
            return render(request,'registroProveedor.html', {'mensaje' : mensaje, 'region':region, 'ciudad':ciudad, 'comuna':comuna, 'rubro':rubro})
        except:
            # Verifica que las claves coincidan
            if clave1 != clave2:               
                mensaje = 'Las contraseñas no coinciden'
                return render(request,'registroProveedor.html', {'mensaje' : mensaje, 'region':region, 'ciudad':ciudad, 'comuna':comuna, 'rubro':rubro})
            # Crear un Usuario
            try:
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
                mensaje = 'Proveedor Creado Exitosamente' # Mensaje de Exito
                return render(request,'registroProveedor.html', {'region':region, 'ciudad':ciudad, 'comuna':comuna, 'rubro':rubro, 'mensaje': mensaje})
            except:
                mensaje = 'Error al Crear Proveedor' # Mensaje de Error
                return render(request,'registroProveedor.html', {'region':region, 'ciudad':ciudad, 'comuna':comuna, 'rubro':rubro, 'mensaje': mensaje})     
    return render(request,'registroProveedor.html', {'region':region, 'ciudad':ciudad, 'comuna':comuna, 'rubro':rubro})

# Añadir al Carro
def add_to_cart(request):
    cart_p={} # Diccionario Carro con los Productos
    cart_p[str(request.GET['prodId'])]={ # Key es la ID
        'nombre':request.GET['nomProd'], # Values con datos a llamar
        'imagen':request.GET['imagen'],
        'cant':request.GET['cant'],
        'precio':request.GET['precio'],
    }
    if 'cartdata' in request.session: # Si existe un Cart 
        if str(request.GET['prodId']) in request.session['cartdata']: # Añadir un producto existente en Carro
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['prodId'])]['cant']=int(cart_p[str(request.GET['prodId'])]['cant'])
            cart_data.update(cart_data)
            request.session['cartdata']=cart_data
        else: # Producto nuevo en carro
            cart_data=request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata']=cart_data
    else:
        request.session['cartdata']=cart_p
    
    return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

# Carro y Concretar Compra
def cart_list(request):
    total_amt = 0
    if request.POST: # Concretar la venta
        doc = request.POST.get("RadioDoc") # Eleccion de Boleta o Factura
        if doc == 'Boleta':
            listaCompra = request.session['cartdata'] # Carro de Compra
            user = request.user # Usuario
            cliente = Cliente.objects.get(idUsuario=user) # Cliente
            for p_id, item in listaCompra.items(): 
                total_amt += int(item['cant']) * int(item['precio']) # Total Boleta
            venta = Venta() # Venta es el Master
            fechaHora = datetime.now()
            venta.fechaVenta = fechaHora
            venta.idCliente = cliente
            venta.total = total_amt
            venta.save()
            for p_id, item in listaCompra.items(): # Generar detalle de Venta
                detalle = Detalle()
                detalle.idVenta = venta
                producto = Producto.objects.get(idProducto = p_id)
                detalle.idProducto = producto
                detalle.precioUnitario = int(item['precio'])
                detalle.cantidad = int(item['cant'])
                detalle.subtotal = detalle.cantidad * detalle.precioUnitario
                detalle.save()
            # Crear Boleta    
            boleta = Boleta()
            boleta.fechaEmision = fechaHora
            boleta.total = venta.total
            boleta.idVenta = venta
            boleta.save()
            # listaDetalle = Detalle.objects.filter(idVenta = venta) 
            # for item in listaDetalle:      
                # prod = item.idProducto_id
                # cant = item.cantidad
                # producto = Producto.objects.get(pk = prod)
                # producto.stock -= cant
                # producto.save() 
            del request.session['cartdata']
            return redirect(reverse('BOLETA', kwargs={'pk':boleta.nroBoleta}))

        elif doc == 'Factura':
            listaCompra = request.session['cartdata'] # Carro de Compra
            user = request.user # Usuario
            cliente = Cliente.objects.get(idUsuario=user) # Cliente
            for p_id, item in listaCompra.items(): 
                total_amt += int(item['cant']) * int(item['precio']) # Total Boleta
            venta = Venta() # Venta es el Master
            fechaHora = datetime.now()
            venta.fechaVenta = fechaHora
            venta.idCliente = cliente
            venta.total = total_amt
            venta.save()
            for p_id, item in listaCompra.items(): # Generar detalle de Venta
                detalle = Detalle()
                detalle.idVenta = venta
                producto = Producto.objects.get(idProducto = p_id)
                detalle.idProducto = producto
                detalle.precioUnitario = int(item['precio'])
                detalle.cantidad = int(item['cant'])
                detalle.subtotal = detalle.cantidad * detalle.precioUnitario
                detalle.save()
            # Crear Factura    
            factura = Factura()
            factura.fechaEmision = fechaHora
            factura.total = venta.total
            factura.idVenta = venta
            factura.iva = int(round(venta.total * 0.19))
            factura.neto = int(factura.total) - int(factura.iva)
            factura.save()
            # listaDetalle = Detalle.objects.filter(idVenta = venta) 
            # for item in listaDetalle:      
                # prod = item.idProducto_id
                # cant = item.cantidad
                # producto = Producto.objects.get(pk = prod)
                # producto.stock -= cant
                # producto.save() 
            del request.session['cartdata']
            return redirect(reverse('FACTURA', kwargs={'pk':factura.nroFactura}))
        else:
            return render(request, 'cart.html')
    else:
        try:
            for p_id,item in request.session['cartdata'].items():
                total_amt+=int(item['cant'])*int(item['precio'])
            return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
        except:
            return render(request, 'cart.html')

# Eliminar del Carro
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

# Actualizar productos en Carro
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

# Listado Boleta
@login_required(login_url='login/')
@group_required('Vendedor')
class ListaBoleta(ListView):
    # Uso de Modelo
    model = Boleta
    template_name = 'listadoBoletas.html'
    context_object_name = 'Boletas'

# Detalle Boleta
@login_required(login_url='login/')
@group_required('Vendedor', 'Cliente')
class BoletaDetail(DetailView):
    context_object_name = 'Boleta_detalle'
    model =  Boleta
    template_name = 'boleta.html'

    def get_context_data(self, *args, **kwargs): # Uso de Context para detalles de Venta
        context = super(BoletaDetail, self).get_context_data(*args, **kwargs)
        context['Detalles'] = Detalle.objects.filter(idVenta_id = self.object.idVenta)
        return context

# Listado Factura
@login_required(login_url='login/')
@group_required('Vendedor')
class ListaFactura(ListView):
    # Uso de Modelo
    model = Factura
    template_name = 'listadoFacturas.html'
    context_object_name = 'Facturas'

# Detalle Factura
@login_required(login_url='login/')
@group_required('Vendedor', 'Cliente')
class FacturaDetail(DetailView):
    context_object_name = 'Factura_detalle'
    model =  Factura
    template_name = 'factura.html'

    def get_context_data(self, *args, **kwargs): # Uso de Context para detalles de Venta
        context = super(FacturaDetail, self).get_context_data(*args, **kwargs)
        context['Detalles'] = Detalle.objects.filter(idVenta_id = self.object.idVenta)
        return context

# Eliminar Boleta
@login_required(login_url='login/')
@group_required('Vendedor')
def borrarBoleta(request, idBoleta):
    nroBoleta = idBoleta 
    boleta = Boleta.objects.get(pk=nroBoleta)
    try:
        boleta.vigente = False
        boleta.save()
        nroVenta = boleta.idVenta_id
        venta = Venta.objects.get(pk=nroVenta)
        venta.valido = False
        venta.save()
        mensaje = 'Boleta Anulada Correctamente'
        return render(request, 'boleta.html', {'object':boleta, 'mensaje': mensaje})
    except:
        mensaje = 'Error al Anular Boleta'
        return render(request, 'boleta.html', {'object':boleta, 'mensaje': mensaje})

# Eliminar Factura
@login_required(login_url='login/')
@group_required('Vendedor')
def borrarFactura(request, idFactura):
    nroFactura = idFactura 
    factura = Factura.objects.get(pk=nroFactura)
    try:
        factura.vigente = False
        factura.save()
        nroVenta = factura.idVenta_id
        venta = Venta.objects.get(pk=nroVenta)
        venta.valido = False
        venta.save()
        mensaje = 'Factura Anulada Correctamente'
        return render(request, 'factura.html', {'object':factura, 'mensaje': mensaje})
    except:
        mensaje = 'Error al Anular Factura'
        return render(request, 'factura.html', {'object':factura, 'mensaje': mensaje})

# Eliminar Orden
@login_required(login_url='login/')
@group_required('Empleado')
def borrarOrden(request, idOrden):
    orden = OrdenCompra.objects.get(pk = idOrden)
    try:
        if orden.recibido == True:
            mensaje = 'Orden de Compra ya recibida. No se puede Anular'
            return render(request, 'ordenDetail.html', {'object':orden, 'mensaje': mensaje})
        orden.valido = False
        orden.save()
        mensaje = 'Orden de Compra Anulada Correctamente'
        return render(request, 'ordenDetail.html', {'object':orden, 'mensaje': mensaje})
    except:
        mensaje = 'Error al Anular Orden'
        return render(request, 'ordenDetail.html', {'object':orden, 'mensaje': mensaje})

# Enviar Orden
@login_required(login_url='login/')
@group_required('Empleado')
def enviarOrden(request, idOrden):
    orden = OrdenCompra.objects.get(pk = idOrden)
    try:
        if orden.enviada == True or orden.valido == False:
            mensaje = 'Orden de Compra ya enviada o anulada. No se puede enviar'
            return render(request, 'ordenDetail.html', {'object':orden, 'mensaje': mensaje})
        orden.enviada = True
        orden.save()
        mensaje = 'Orden de Compra enviada correctamente'
        return render(request, 'ordenDetail.html', {'object':orden, 'mensaje': mensaje})
    except:
        mensaje = 'Error al Enviar Orden'
        return render(request, 'ordenDetail.html', {'object':orden, 'mensaje': mensaje})

# Recibir Orden
@login_required(login_url='login/')
@group_required('Empleado')
def recibirOrden(request, idOrden):
    orden = OrdenCompra.objects.get(pk = idOrden)
    try:
        if orden.enviada == False or orden.valido == False or orden.recibido == True:
            mensaje = 'Orden de Compra ya recibida o anulada. No se puede recibir'
            return render(request, 'ordenDetail.html', {'object':orden, 'mensaje': mensaje})
        orden.recibido = True
        orden.save()
        mensaje = 'Orden de Compra recibida correctamente'
        # prod = orden.idProducto_id
        # cant= orden.cantidad
        # producto = Producto.objects.get(pk = prod)
        # producto.stock += cant
        # producto.save() 
        return render(request, 'ordenDetail.html', {'object':orden, 'mensaje': mensaje})
    except:
        mensaje = 'Error al Recibir Orden'
        return render(request, 'ordenDetail.html', {'object':orden, 'mensaje': mensaje})
