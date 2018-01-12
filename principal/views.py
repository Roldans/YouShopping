# Create your views here.

from principal.models import Producto
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.urls import reverse
from django.views import generic

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'lista': productos})

def ver_producto(request, product):
    producto = get_object_or_404(Producto, product=product)
#     recomendados = 
#     return render(request, 'ver_producto.html', {'producto': producto, recomendados[:5]})
    return render(request, 'ver_producto.html', {'producto': producto})