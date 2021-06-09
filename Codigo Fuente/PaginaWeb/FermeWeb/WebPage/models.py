from django.db import models
from django.contrib.auth.models import Group, User


# Create your models here.

# FamiliaProducto
class FamiliaProducto(models.Model):
    idFamiliaProducto = models.AutoField(primary_key = True)
    descripcion = models.CharField(max_length = 40)
    
    def __str__(self):
        return self.descripcion

#Tipo Producto      
class TipoProducto(models.Model):

    idTipoProducto = models.AutoField(primary_key = True)
    descripcion = models.CharField(max_length = 40)
    idFamProducto = models.ForeignKey(FamiliaProducto, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.descripcion

# Rubro
class Rubro(models.Model):
    
    idRubro = models.AutoField(primary_key = True)
    rubro = models.CharField(max_length = 30)

    def __str__(self):
        return self.rubro
    
# Cargo
class Cargo(models.Model):

    idCargo = models.AutoField(primary_key = True)
    cargo = models.CharField(max_length = 20)

    def __str__(self):
        return self.cargo

# Region
class Region(models.Model):

    idRegion = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 30)

    def __str__(self):
        return self.nombre
    
# Ciudad
class Ciudad(models.Model):

    idCiudad = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 30)
    idRegion = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
# Comuna
class Comuna(models.Model):

    idComuna = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 30)
    idCiudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

# Persona
class Persona(models.Model):
    
    rut = models.CharField(max_length = 10)
    nombres = models.CharField(max_length = 30)
    apellidoPaterno = models.CharField(max_length = 20, null= True)
    apellidoMaterno = models.CharField(max_length = 20, null= True)
    telefono = models.CharField(max_length = 9)
    direccion = models.CharField(max_length = 40)
    idComuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    idUsuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True
        

# Cliente
class Cliente(Persona):
    idCliente = models.AutoField(primary_key = True)
    email = models.CharField(max_length = 40)

    def __str__(self):
        nombre = self.nombres + ' ' + self.apellidoPaterno + ' ' + self.apellidoMaterno
        return nombre
    
# Proveedor
class Proveedor(Persona):

    idProveedor = models.AutoField(primary_key = True)
    representante = models.CharField(max_length = 50)
    idRubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)

    def __str__(self):
        nombre = self.nombres 
        return nombre

# Empleado
class Empleado(Persona):
    
    idEmpleado = models.AutoField(primary_key = True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

    def __str__(self):
        nombre = self.nombres + ' ' + self.apellidoPaterno + ' ' + self.apellidoMaterno
        return nombre

# Producto
class Producto(models.Model):

    idProducto = models.CharField(max_length = 17, primary_key = True)
    nombre = models.CharField(max_length = 30)
    descripcion = models.CharField(max_length = 200)
    precio = models.IntegerField()
    stock = models.IntegerField()
    stockCrit = models.IntegerField()
    imagen = models.ImageField(upload_to='productos', default='not_found.jpg')
    fVenc = models.DateField(auto_now=False, auto_now_add=False, null=True)
    idFamProducto = models.ForeignKey(FamiliaProducto, on_delete=models.CASCADE)
    idTipoProducto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    idProveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# Orden Compra
class OrdenCompra(models.Model):

    idOrdenCompra = models.AutoField(primary_key = True)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    total = models.IntegerField()
    comentario = models.CharField(max_length = 200, blank= True)
    fechaPedido = models.DateTimeField(auto_now=False, auto_now_add=False)
    idEmpleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    enviada = models.BooleanField(default=False)
    recibido = models.BooleanField(default=False)
    valido = models.BooleanField(default=True)
    
    def __str__(self):
        nombre = ''
        nombre = nombre + 'Orden Compra ' + str(self.idOrdenCompra) + ' de Producto ' + str(self.idProducto)
        return nombre

# OrdenVenta (Master)
class Venta(models.Model):

    idVenta = models.AutoField(primary_key = True)
    fechaVenta = models.DateTimeField(auto_now=False, auto_now_add=False)
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total = models.IntegerField()
    valido = models.BooleanField(default=True)

    def __str__(self):
        nombre = ''
        nombre = nombre + 'Venta ' + str(self.idVenta) + ' en Fecha ' + str(self.fechaVenta)
        return nombre

# Detalle (Slave)
class Detalle(models.Model):
    
    idDetalle = models.AutoField(primary_key = True)
    idVenta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precioUnitario = models.IntegerField()
    subtotal = models.IntegerField()

    def __str__(self):
        nombre = ''
        nombre = nombre + 'Detalle Venta ' + str(self.idDetalle) + ' de Venta ' + str(self.idVenta)
        return nombre
    
# Boleta
class Boleta(models.Model):
    
    nroBoleta = models.AutoField(primary_key = True)
    fechaEmision = models.DateTimeField(auto_now=False, auto_now_add=False)
    total = models.IntegerField()
    idVenta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    vigente = models.BooleanField(default = True)

    def __str__(self):
        nombre = ''
        nombre = nombre + 'Boleta nro' + str(self.nroBoleta)
        return nombre

# Factura
class Factura(models.Model):

    nroFactura = models.AutoField(primary_key = True)
    fechaEmision = models.DateTimeField(auto_now=False, auto_now_add=False)
    neto = models.IntegerField()
    iva = models.IntegerField()
    total = models.IntegerField()
    idVenta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    vigente = models.BooleanField(default = True)

    def __str__(self):
        nombre = ''
        nombre = nombre + 'Factura nro' + str(self.nroFactura)
        return nombre
    



