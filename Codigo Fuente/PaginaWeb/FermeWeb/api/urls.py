from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns= [
    url(r'^api/productos/$', views.ProductoViewSet.as_view())
]