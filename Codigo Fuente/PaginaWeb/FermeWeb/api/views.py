from django.shortcuts import render

from WebPage.models import Producto
from .serializers import ProductoSerializer
from rest_framework import generics

# Create your views here.
class ProductoViewSet(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
