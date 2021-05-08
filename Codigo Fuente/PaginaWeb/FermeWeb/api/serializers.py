

from WebPage.models import Producto
from rest_framework import serializers

#Modelo a serializar

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["nombre","descripcion","precio","stock", "stockCrit", "fVenc","idFamProducto","idTipoProducto","idProveedor","imagen"]