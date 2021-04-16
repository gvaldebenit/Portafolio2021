from django.db import models

# Create your models here.

# Slider Herramientas
class sliderHerramienta(models.Model):

    idSlider = models.CharField(max_length = 15, primary_key = True)
    imagen = models.ImageField(upload_to = 'herramientas')

    def __str__(self):
        return self.idSlider  

# Slider Pinturas
class sliderPintura(models.Model):

    idSlider = models.CharField(max_length = 15, primary_key = True)
    imagen = models.ImageField(upload_to = 'pinturas')

    def __str__(self):
        return self.idSlider

# Slider Materiales
class sliderMateriales(models.Model):

    idSlider = models.CharField(max_length = 15, primary_key = True)
    imagen = models.ImageField(upload_to = 'materiales')

    def __str__(self):
        return self.idSlider

# Producto
