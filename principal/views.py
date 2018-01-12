# Create your views here.

import os

from django.shortcuts import render, get_object_or_404

from principal.models import Producto

import RS_SoloItems


def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'listar_productos.html', {'lista': productos})

def ver_producto(request):
    id = int(request.GET.get('id',None))
    producto = get_object_or_404(Producto, id=id)
    recomendados = []
    for item in RS_SoloItems.getRecommendedItems(id):
        print item[-1]
        recomendados.append(Producto.objects.get(id=item[-1]))
    return render(request, 'ver_producto.html', {'producto': producto, 'recomendados': recomendados})

