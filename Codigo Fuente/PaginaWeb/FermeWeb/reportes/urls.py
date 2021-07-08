"""FermeWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views

from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name="REPOINDEX"),
    path('venta', venta, name="REPOVENTA"),
    path('visita', visita, name="REPOVISITA"),
    path('ajax/producto/stock', StockProducto),
    path('ajax/ventas/today', ventasToday),
    path('ajax/ventas/week', ventasWeek),
    path('ajax/ventas/moth', ventasMonth),
    path('ajax/ventas/year', ventasYear),
    path('ajax/ventas/doc/today', ventasDocToday),
    path('ajax/ventas/doc/week', ventasDocWeek),
    path('ajax/ventas/doc/month', ventasDocMonth),
    path('ajax/ventas/doc/year', ventasDocYear),
    path('ajax/visitas/today', visitasToday),
    path('ajax/visitas/week', visitasWeek),
    path('ajax/visitas/month', visitasMonth),
]
