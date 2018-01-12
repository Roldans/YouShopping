# Create your views here.

from principal.models import Producto
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext

def listar_productos(request):
    productos = Producto.objects.all()
    return render_to_response('lista_productos.html', {'lista': productos})
