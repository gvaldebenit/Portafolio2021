from django.http.response import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.db.models import Q, F, Sum, Count
from datetime import datetime, timedelta
from django.db.models.functions import TruncHour, TruncDay
from WebPage.models import *
from reportes.models import *


# Create your views here.

def index(request):
    return render(request,'reportes/producto.html')

def venta(request):
    return render(request,'reportes/ventas.html')

def visita(request):
    return render(request, 'reportes/visitas.html')

# Grafico Productos
def StockProducto(request):
    data = [['Producto', 'Stock', 'Familia Producto', 'Tipo Producto']]
    query = Producto.objects.order_by('nombre')
    for item in query:
        row = []
        row.append(item.nombre)
        row.append(item.stock)
        row.append(item.idFamProducto.descripcion)
        row.append(item.idTipoProducto.descripcion)
        data.append(row)
    return JsonResponse(data, safe=False)

# Json para Ajax de ventas del dia
def ventasToday(request):
    sql_query = '''SELECT d.idDetalle, p.nombre AS nombre, sum(d.cantidad) AS cantidad, sum(d.subtotal) AS total, f.descripcion AS familia
    FROM WebPage_detalle d 
    JOIN WebPage_producto p ON d.idProducto_id = p.idProducto
    JOIN WebPage_venta v ON d.idVenta_id = v.idVenta
    JOIN WebPage_familiaproducto f ON p.idFamProducto_id = f.idFamiliaProducto
    WHERE v.valido = True 
    AND v.fechaVenta BETWEEN DATE('now', '-1 day') AND DATE('now')
    GROUP BY d.idProducto_id'''
    data = [['Producto', 'Cantidad', 'Venta', 'Familia Producto']]
    query = Detalle.objects.raw(sql_query)
    for item in query:
        row = []
        row.append(item.nombre)
        row.append(item.cantidad)
        row.append(item.total)
        row.append(item.familia)
        data.append(row)
    return JsonResponse(data, safe=False)

# JSON para Ajax de Ventas desde Inicio de la Semana
def ventasWeek(request):
    sql_query = '''SELECT d.idDetalle, p.nombre AS nombre, sum(d.cantidad) AS cantidad, sum(d.subtotal) AS total, f.descripcion AS familia
    FROM WebPage_detalle d 
    JOIN WebPage_producto p ON d.idProducto_id = p.idProducto
    JOIN WebPage_venta v ON d.idVenta_id = v.idVenta
    JOIN WebPage_familiaproducto f ON p.idFamProducto_id = f.idFamiliaProducto
    WHERE v.valido = True 
    AND v.fechaVenta BETWEEN DATE('now', 'weekday 1', '-7 days') AND DATE('now')
    GROUP BY d.idProducto_id'''
    data = [['Producto', 'Cantidad', 'Venta', 'Familia Producto']]
    query = Detalle.objects.raw(sql_query)
    for item in query:
        row = []
        row.append(item.nombre)
        row.append(item.cantidad)
        row.append(item.total)
        row.append(item.familia)
        data.append(row)
    return JsonResponse(data, safe=False)

# JSON para Ajax de Ventas desde Inicio de Mes
def ventasMonth(request):
    sql_query = '''SELECT d.idDetalle, p.nombre AS nombre, sum(d.cantidad) AS cantidad, sum(d.subtotal) AS total, f.descripcion AS familia
    FROM WebPage_detalle d 
    JOIN WebPage_producto p ON d.idProducto_id = p.idProducto
    JOIN WebPage_venta v ON d.idVenta_id = v.idVenta
    JOIN WebPage_familiaproducto f ON p.idFamProducto_id = f.idFamiliaProducto
    WHERE v.valido = True 
    AND v.fechaVenta BETWEEN DATE('now', 'start of month') AND DATE('now')
    GROUP BY d.idProducto_id'''
    data = [['Producto', 'Cantidad', 'Venta', 'Familia Producto']]
    query = Detalle.objects.raw(sql_query)
    for item in query:
        row = []
        row.append(item.nombre)
        row.append(item.cantidad)
        row.append(item.total)
        row.append(item.familia)
        data.append(row)
    return JsonResponse(data, safe=False)

# JSON para Ajax de Ventas desde Inicio de Año
def ventasYear(request):
    sql_query = '''SELECT d.idDetalle, p.nombre AS nombre, sum(d.cantidad) AS cantidad, sum(d.subtotal) AS total, f.descripcion AS familia
    FROM WebPage_detalle d 
    JOIN WebPage_producto p ON d.idProducto_id = p.idProducto
    JOIN WebPage_venta v ON d.idVenta_id = v.idVenta
    JOIN WebPage_familiaproducto f ON p.idFamProducto_id = f.idFamiliaProducto
    WHERE v.valido = True 
    AND v.fechaVenta BETWEEN DATE('now', 'start of year') AND DATE('now')
    GROUP BY d.idProducto_id'''
    data = [['Producto', 'Cantidad', 'Venta', 'Familia Producto']]
    query = Detalle.objects.raw(sql_query)
    for item in query:
        row = []
        row.append(item.nombre)
        row.append(item.cantidad)
        row.append(item.total)
        row.append(item.familia)
        data.append(row)
    return JsonResponse(data, safe=False)

# Json para Ajax de ventas de Docs del dia
def ventasDocToday(request):
    now = datetime.now()
    start = (datetime.now() - timedelta(days = 1))
    data = [['Documento', 'Cantidad', 'Venta']]
    query_boleta = Boleta.objects.filter(vigente = True, fechaEmision__lte= now, fechaEmision__gte= start)
    query_factura = Factura.objects.filter(vigente = True, fechaEmision__lte= now, fechaEmision__gte= start)
    if query_boleta.count() > 0 and query_factura.count() > 0:
        # Boleta
        row = []
        row.append('Boleta')
        row.append(query_boleta.count())
        row.append(query_boleta.aggregate(Sum('total'))['total__sum'])
        data.append(row)
        # Factura
        row = []
        row.append('Factura')
        row.append(query_factura.count())
        row.append(query_factura.aggregate(Sum('total'))['total__sum'])
        data.append(row)
    elif query_boleta.count() <= 0 and query_factura.count() > 0:
        # Boleta
        row = []
        row.append('Boleta')
        row.append(0)
        row.append(0)
        data.append(row)
        # Factura
        row = []
        row.append('Factura')
        row.append(query_factura.count())
        row.append(query_factura.aggregate(Sum('total'))['total__sum'])
        data.append(row)
    elif query_boleta.count() > 0 and query_factura.count() <= 0:
        # Boleta
        row = []
        row.append('Boleta')
        row.append(query_boleta.count())
        row.append(query_boleta.aggregate(Sum('total'))['total__sum'])
        data.append(row)
        # Factura
        row = []
        row.append('Factura')
        row.append(0)
        row.append(0)
        data.append(row)
    else:
        pass       
    return JsonResponse(data, safe=False)

# JSON para Ajax de Ventas de Docs desde Inicio de la Semana
def ventasDocWeek(request):
    now = datetime.now()
    start = (datetime.now() - timedelta(days=now.weekday()))
    data = [['Documento', 'Cantidad', 'Venta']]
    query_boleta = Boleta.objects.filter(vigente = True, fechaEmision__lte= now, fechaEmision__gte= start)
    query_factura = Factura.objects.filter(vigente = True, fechaEmision__lte= now, fechaEmision__gte= start)
    if query_boleta.count() > 0 and query_factura.count() > 0:
        # Boleta
        row = []
        row.append('Boleta')
        row.append(query_boleta.count())
        row.append(query_boleta.aggregate(Sum('total'))['total__sum'])
        data.append(row)
        # Factura
        row = []
        row.append('Factura')
        row.append(query_factura.count())
        row.append(query_factura.aggregate(Sum('total'))['total__sum'])
        data.append(row)
    elif query_boleta.count() <= 0 and query_factura.count() > 0:
        # Boleta
        row = []
        row.append('Boleta')
        row.append(0)
        row.append(0)
        data.append(row)
        # Factura
        row = []
        row.append('Factura')
        row.append(query_factura.count())
        row.append(query_factura.aggregate(Sum('total'))['total__sum'])
        data.append(row)
    elif query_boleta.count() > 0 and query_factura.count() <= 0:
        # Boleta
        row = []
        row.append('Boleta')
        row.append(query_boleta.count())
        row.append(query_boleta.aggregate(Sum('total'))['total__sum'])
        data.append(row)
        # Factura
        row = []
        row.append('Factura')
        row.append(0)
        row.append(0)
        data.append(row)
    else:
        pass      
    return JsonResponse(data, safe=False)

# JSON para Ajax de Ventas de Docs desde Inicio de Mes
def ventasDocMonth(request):
    now = datetime.now()
    start = now.replace(day=1)
    data = [['Documento', 'Cantidad', 'Venta']]
    query_boleta = Boleta.objects.filter(vigente = True, fechaEmision__lte= now, fechaEmision__gte= start)
    query_factura = Factura.objects.filter(vigente = True, fechaEmision__lte= now, fechaEmision__gte= start)
    if query_boleta.count() > 0 and query_factura.count() > 0:
        # Boleta
        row = []
        row.append('Boleta')
        row.append(query_boleta.count())
        row.append(query_boleta.aggregate(Sum('total'))['total__sum'])
        data.append(row)
        # Factura
        row = []
        row.append('Factura')
        row.append(query_factura.count())
        row.append(query_factura.aggregate(Sum('total'))['total__sum'])
        data.append(row)
    elif query_boleta.count() <= 0 and query_factura.count() > 0:
        # Boleta
        row = []
        row.append('Boleta')
        row.append(0)
        row.append(0)
        data.append(row)
        # Factura
        row = []
        row.append('Factura')
        row.append(query_factura.count())
        row.append(query_factura.aggregate(Sum('total'))['total__sum'])
        data.append(row)
    elif query_boleta.count() > 0 and query_factura.count() <= 0:
        # Boleta
        row = []
        row.append('Boleta')
        row.append(query_boleta.count())
        row.append(query_boleta.aggregate(Sum('total'))['total__sum'])
        data.append(row)
        # Factura
        row = []
        row.append('Factura')
        row.append(0)
        row.append(0)
        data.append(row)
    else:
        pass       
    return JsonResponse(data, safe=False)

# JSON para Ajax de Ventas de Docs desde Inicio de Año
def ventasDocYear(request):
    now = datetime.now()
    start = now.replace(month=1, day=1)
    data = [['Documento', 'Cantidad', 'Venta']]
    query_boleta = Boleta.objects.filter(vigente = True, fechaEmision__lte= now, fechaEmision__gte= start)
    query_factura = Factura.objects.filter(vigente = True, fechaEmision__lte= now, fechaEmision__gte= start)
    if query_boleta.count() > 0 and query_factura.count() > 0:
        # Boleta
        row = []
        row.append('Boleta')
        row.append(query_boleta.count())
        row.append(query_boleta.aggregate(Sum('total'))['total__sum'])
        data.append(row)
        # Factura
        row = []
        row.append('Factura')
        row.append(query_factura.count())
        row.append(query_factura.aggregate(Sum('total'))['total__sum'])
        data.append(row)
    elif query_boleta.count() <= 0 and query_factura.count() > 0:
        # Boleta
        row = []
        row.append('Boleta')
        row.append(0)
        row.append(0)
        data.append(row)
        # Factura
        row = []
        row.append('Factura')
        row.append(query_factura.count())
        row.append(query_factura.aggregate(Sum('total'))['total__sum'])
        data.append(row)
    elif query_boleta.count() > 0 and query_factura.count() <= 0:
        # Boleta
        row = []
        row.append('Boleta')
        row.append(query_boleta.count())
        row.append(query_boleta.aggregate(Sum('total'))['total__sum'])
        data.append(row)
        # Factura
        row = []
        row.append('Factura')
        row.append(0)
        row.append(0)
        data.append(row)
    else:
        pass    
    return JsonResponse(data, safe=False)

def visitasToday(request):
    now = datetime.now()
    start = now.replace(hour=0, minute=0, second=0)
    data = [['Hora', 'Usuarios Autenticados', 'Usuarios Anonimos']]
    query = Visita.objects.filter(timestamp__range=(start, now)
        ).annotate(
            hour=TruncHour('timestamp')
        ).values(
            'hour'
        ).annotate(
            total_auth=Count('id', filter=Q(user__isnull=False)),
            total_anon=Count('id', filter=Q(user__isnull=True))
        ).values(
            'hour', 'total_auth','total_anon'
        )
    for item in query:
        row = []
        row.append(item['hour'].strftime("%d/%m/%y %H:%M"))
        row.append(item['total_auth'])
        row.append(item['total_anon'])
        data.append(row)
    return JsonResponse(data, safe=False)

def visitasWeek(request):
    now = datetime.now()
    start = (datetime.now() - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0)
    data = [['Hora', 'Usuarios Autenticados', 'Usuarios Anonimos']]
    query = Visita.objects.filter(timestamp__range=(start, now)
        ).annotate(
            hour=TruncHour('timestamp')
        ).values(
            'hour'
        ).annotate(
            total_auth=Count('id', filter=Q(user__isnull=False)),
            total_anon=Count('id', filter=Q(user__isnull=True))
        ).values(
            'hour', 'total_auth','total_anon'
        )
    for item in query:
        row = []
        row.append(item['hour'].strftime("%d/%m/%y %H:%M"))
        row.append(item['total_auth'])
        row.append(item['total_anon'])
        data.append(row)
    return JsonResponse(data, safe=False)

def visitasMonth(request):
    now = datetime.now()
    start = now.replace(day=1,hour=0, minute=0, second=0)
    data = [['Hora', 'Usuarios Autenticados', 'Usuarios Anonimos']]
    query = Visita.objects.filter(timestamp__range=(start, now)
        ).annotate(
            hour=TruncDay('timestamp')
        ).values(
            'hour'
        ).annotate(
            total_auth=Count('id', filter=Q(user__isnull=False)),
            total_anon=Count('id', filter=Q(user__isnull=True))
        ).values(
            'hour', 'total_auth','total_anon'
        )
    for item in query:
        row = []
        row.append(item['hour'].strftime("%d/%m/%y %H:%M"))
        row.append(item['total_auth'])
        row.append(item['total_anon'])
        data.append(row)
    return JsonResponse(data, safe=False)