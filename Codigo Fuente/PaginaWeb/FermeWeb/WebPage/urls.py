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
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name = "INDEX"),
    path('login', login, name = "LOGIN"),
    path('logout', logoutView, name = "LOGOUT"),
    path('signup', signup, name = "SIGNUP"),
    path('',include('api.urls')),
    path('registro_producto', registroProducto, name = "REGP"),
    path('buscar/', ResultadosBusqueda.as_view(), name='BUSCAR'),
    path('ayuda', ayuda, name = "AYUDA"),
    path('misionyvision', misionyvision, name = "MISIONYVISION"),
    #path('item/<id>', item, name = "ITEM")
    path('item/<pk>', ItemDetail.as_view(), name= "ITEM"),
]
