from django.db import models

# Create your models here.

# Slider Herramientas
class SliderHerramienta(models.Model):

    idSlider = models.CharField(max_length = 15, primary_key = True)
    imagen = models.ImageField(upload_to = 'herramientas')

    def __str__(self):
        return self.idSlider  

# Slider Pinturas
class SliderPintura(models.Model):

    idSlider = models.CharField(max_length = 15, primary_key = True)
    imagen = models.ImageField(upload_to = 'pinturas')

    def __str__(self):
        return self.idSlider

# Slider Materiales
class SliderMateriales(models.Model):

    idSlider = models.CharField(max_length = 15, primary_key = True)
    imagen = models.ImageField(upload_to = 'materiales')

    def __str__(self):
        return self.idSlider

# TipoProducto
class TipoProducto(models.Model):

    descripcion = models.CharField(max_length = 40)


# FamiliaProducto
class FamiliaProducto(models.Model):

    descripcion = models.CharField(max_length = 40)

# Rubro
class Rubro(models.Model):

    rubro = models.CharField(max_length = 30)
    
# Cargo
class Cargo(models.Model):

    cargo = models.CharField(max_length = 20)
    
# Persona
class Persona(models.Model):
    
    rut = models.CharField(max_length = 10)
    nombres = models.CharField(max_length = 30)
    apellidoPaterno = models.CharField(max_length = 20)
    apellidoMaterno = models.CharField(max_length = 20)
    telefono = models.CharField(max_length = 9)
    direccion = models.CharField(max_length = 40)
    
    class Meta:
        abstract = True

# Producto
class Producto(models.Model):

    idProducto = models.CharField(primary_key = true)
    nombre = models.CharField(max_length = 30)
    descripcion = models.CharField(max_length = 200)
    precio = models.IntegerField()
    stock = models.IntegerField()
    stockCrit = models.IntegerField()
    fVenc = models.DateField(auto_now=False, auto_now_add=False)
    idFamProducto = models.ForeignKey(FamiliaProducto, on_delete=models.CASCADE)
    idTipoProducto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    idProveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

# Cliente
class Cliente(Persona):

    email = models.CharField(max_length = 40)
    
# Proveedor
class Proveedor(Persona):

    apellidoPaterno = models.CharField(null = true)
    apellidoMaterno = models.CharField(null = true)
    representante = models.CharField(max_length = 50)
    idRubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)

# Empleado
class Empleado(Persona):
    
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    
# Orden Compra
class OrdenCompra(models.Model):

    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    total = models.IntegerField()
    comentario = models.CharField(max_length = 200)
    idEmpleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

# OrdenVenta (Master)
class Venta(models.Model):

    fechaVenta = models.DateTimeField(auto_now=False, auto_now_add=False)
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total = models.IntegerField()
    estado = models.IntegerField()

# Detalle (Slave)
class Detalle(models.Model):

    idVenta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precioUnitario = models.IntegerField()
    subtotal = models.IntegerField()
    
# Boleta
class Boleta(models.Model):
    
    nroBoleta = models.AutoField(primary_key = True)
    fechaEmision = models.DateTimeField(auto_now=False, auto_now_add=False)
    totalBoleta = models.IntegerField()
    idVenta = models.ForeignKey(Venta, on_delete=models.CASCADE)


# Factura
class Factura(models.Model):

    nroFactura = models.AutoField(primary_key = True)
    fechaEmision = models.DateTimeField(auto_now=False, auto_now_add=False)
    neto = models.IntegerField()
    iva = models.IntegerField()
    total = models.IntegerField()
    idVenta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    
# Region
class Region(models.Model):

    nombre = models.CharField(max_length = 30)
    
# Ciudad
class Ciudad(models.Model):

    nombre = models.CharField(max_length = 30)
    idRegion = models.ForeignKey(Region, on_delete=models.CASCADE)
    
# Comuna
class Comuna(models.Model):

    nombre = models.CharField(max_length = 30)
    idCiudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    
# TipoUsuario?
 

    
