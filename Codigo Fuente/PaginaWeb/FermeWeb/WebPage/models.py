from django.db import models

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
        
    def __str__(self):
        return self.nombres

# Cliente
class Cliente(Persona):
    idCliente = models.AutoField(primary_key = True)
    email = models.CharField(max_length = 40)
    
# Proveedor
class Proveedor(Persona):

    idProveedor = models.AutoField(primary_key = True)
    representante = models.CharField(max_length = 50)
    idRubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)



# Empleado
class Empleado(Persona):
    
    idEmpleado = models.AutoField(primary_key = True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

    def __str__(self):
        return self.cargo

# Producto
class Producto(models.Model):

    idProducto = models.CharField(max_length = 17, primary_key = True)
    nombre = models.CharField(max_length = 30)
    descripcion = models.CharField(max_length = 200)
    precio = models.IntegerField()
    stock = models.IntegerField()
    stockCrit = models.IntegerField()
    fVenc = models.DateField(auto_now=False, auto_now_add=False)
    idFamProducto = models.ForeignKey(FamiliaProducto, on_delete=models.CASCADE)
    idTipoProducto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    idProveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    imagen=models.ImageField(upload_to='productos',null=True)

    def __str__(self):
        return self.nombre


# Orden Compra
class OrdenCompra(models.Model):

    idOrdenCompra = models.AutoField(primary_key = True)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    total = models.IntegerField()
    comentario = models.CharField(max_length = 200, blank= True)
    idEmpleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

# OrdenVenta (Master)
class Venta(models.Model):

    idVenta = models.AutoField(primary_key = True)
    fechaVenta = models.DateTimeField(auto_now=False, auto_now_add=False)
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total = models.IntegerField()
    estado = models.IntegerField()

# Detalle (Slave)
class Detalle(models.Model):
    
    idDetalle = models.AutoField(primary_key = True)
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

    idRegion = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 30)
    
# Ciudad
class Ciudad(models.Model):

    idCiudad = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 30)
    idRegion = models.ForeignKey(Region, on_delete=models.CASCADE)
    
# Comuna
class Comuna(models.Model):

    idComuna = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 30)
    idCiudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    
# TipoUsuario?
 

    
