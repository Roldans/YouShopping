# Create your views here.

import os
from django.shortcuts import render, get_object_or_404
from principal.models import Producto
from django.core.paginator import Paginator
from django.http import Http404
import RS_SoloItems
from django.template.context import RequestContext


def listar_productos(request):
    productos = Producto.objects.all()
    max = len(productos)
    page = int(request.GET.get('page', 1))
    if page > max:
        raise Http404
    productos = Paginator(productos, 5)
    return render(request, 'listar_productos.html', {'lista': productos.page(page)}, context_instance=RequestContext(request))

def ver_producto(request):
    id = int(request.GET.get('id', None))
    producto = get_object_or_404(Producto, id=id)
    recomendados = []
    for item in RS_SoloItems.getRecommendedItems(id):
        print item[-1]
        recomendados.append(Producto.objects.get(id=item[-1]))
    return render(request, 'ver_producto.html', {'producto': producto, 'recomendados': recomendados})

