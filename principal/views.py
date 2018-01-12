# Create your views here.

from principal.models import Producto
from django.shortcuts import render, get_object_or_404

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'listar_productos.html', {'lista': productos})

def ver_producto(request):
    producto = get_object_or_404(Producto, id=int(request.GET.get('id',None)))
#     recomendados = 
#     return render(request, 'ver_producto.html', {'producto': producto, recomendados[:5]})
    return render(request, 'ver_producto.html', {'producto': producto})