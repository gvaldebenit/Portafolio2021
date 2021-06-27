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
    path('', index, name = "INDEX"),
    path('login', login, name = "LOGIN"),
    path('logout', logoutView, name = "LOGOUT"),
    path('signup', signup, name = "SIGNUP"),
    path('',include('api.urls')),
    path('registro_producto', registroProducto, name = "REGP"),
    path('buscar/', ResultadosBusqueda.as_view(), name='BUSCAR'),
    path('ayuda', ayuda, name = "AYUDA"),
    path('misionyvision', misionyvision, name = "MISIONYVISION"),
    path('item/<pk>', ItemDetail.as_view(), name= "ITEM"),
    path('pinturas/', ListaPinturas.as_view(), name='PINTURAS'),
    path('herramientas/', ListaHerramienta.as_view(), name='HERRAMIENTAS'),
    path('materiales/', ListaMateriales.as_view(), name='MATERIALES'),
    path('otros/', ListaOtros.as_view(), name='OTROS'),
    path('contacto', contacto, name = "CONTACTO"),
    path('orden_compra', encargarProducto, name = 'ORDENCOMPRA'),
    path('orden_compra/<str:id_prod>', encargarProducto, name = 'ORDENCOMPRA'),
    path('listado_ordenCompra', ListaOrdenCompra.as_view(), name='LISTORDENCOMPRA'),
    path('ordenCompra/<pk>', OrdenCompraDetail.as_view(), name="ORDENDETAIL"),
    path('registro_proveedor', crearProveedor, name='REGPROV'),
    path('add-to-cart', views.add_to_cart, name = 'add_to_cart'),
    path('cart', views.cart_list, name = 'cart'),
    path('delete-from-cart', views.delete_cart_item, name = 'delete-from-cart'),
    path('update-cart',views.update_cart_item,name='update-cart'),
    path('listado_boleta', ListaBoleta.as_view(), name="LISTABOLETA"),
    path('listado_factura', ListaFactura.as_view(), name="LISTAFACTURA"),
    path('boleta/<pk>', BoletaDetail.as_view(), name="BOLETA"),
    path('factura/<pk>', FacturaDetail.as_view(), name="FACTURA"),
    path('del_boleta/<idBoleta>', borrarBoleta, name="DELBOLETA"),
    path('del_factura/<idFactura>', borrarFactura, name="DELFACTURA"),
    path('del_orden/<idOrden>', borrarOrden, name="DELORDEN"),
    path('env_orden/<idOrden>', enviarOrden, name="ENVORDEN"),
    path('rec_orden/<idOrden>', recibirOrden, name="RECIBORDEN"),
    
]
