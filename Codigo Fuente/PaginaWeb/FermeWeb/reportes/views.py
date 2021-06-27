from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.db.models import Q, F
from WebPage.models import *

# Create your views here.

def index(request):
    return render(request,'reportes/producto.html')

# Añadir al Carro
def grafico(request):
    data = [['Producto', 'Stock']]
    query = Producto.objects.all()
    for item in query:
        row = []
        row.append(item.nombre)
        row.append(item.stock)
        data.append(row)
    return JsonResponse(data, safe=False)
