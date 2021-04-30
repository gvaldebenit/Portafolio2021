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

# Proveedor
class Proveedor(models.Model):

    rut = models.CharField(max_length = 10)
    nombre = models.CharField(max_length = 20)
    representante = models.CharField(max_length = 50)
    telefono = models.CharField(max_length = 30)
    direccion = models.CharField(max_length = 40)

# Producto
class Producto(models.Model):

    nombre = models.CharField(max_length = 30)
    descripcion = models.CharField(max_length = 200)
    precio = models.IntegerField()
    stock = models.IntegerField()
    stockCrit = models.IntegerField()
    fVenc = models.DateField(auto_now=False, auto_now_add=False)
    idFamProducto = models.ForeignKey(FamiliaProducto, on_delete=models.CASCADE)
    idTipoProducto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    idProveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)


    
