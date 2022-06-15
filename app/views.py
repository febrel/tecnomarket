from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto,Marca
from .forms import ContactoForm, ProductoForms, CustomUserCreationForm
from django.contrib import messages
# Para paginador
from django.core.paginator import Paginator
from django.http import Http404

# Para authenticar el registro login
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required

# REST
from rest_framework import viewsets
from .serializers import ProductoSerializer, MarcaSerializer

# Create your views here.


# REST
class MarcaViewSet(viewsets.ModelViewSet):
     queryset = Marca.objects.all()
     serializer_class = MarcaSerializer



class ProductoViewSet(viewsets.ModelViewSet):
    
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    # Para filtrar utilizo la funcion (?nombre = televisor)
    def get_queryset(self):
        productos = Producto.objects.all()
        nombre = self.request.GET.get('nombre')

        if(nombre):
            # __contains = (like DB)
            productos = productos.filter(nombre__contains=nombre)

        return productos


@login_required
def home(request):
    productos = Producto.objects.all()

    data = {
        'productos': productos
    }

    return render(request, 'app/home.html', data)

@login_required
def contacto(request):

    data = {
        'form': ContactoForm()
    }

    # Si llegan datos por POST
    if(request.method == 'POST'):
        formulario = ContactoForm(data=request.POST)
        # Si es valido guarda
        if(formulario.is_valid()):
            formulario.save()
            data['mensaje'] = 'Contacto guardado'
        else:
            data['form'] = formulario

    return render(request, 'app/contacto.html', data)


@login_required
def galeria(request):

    return render(request, 'app/galeria.html')


@permission_required('app.add_producto')
def agregarProducto(request):
    data = {
        'form': ProductoForms()
    }

    # Si llegan datos por POST
    if(request.method == 'POST'):
        formulario = ProductoForms(data=request.POST, files=request.FILES)
        # Si es valido guarda
        if(formulario.is_valid()):
            formulario.save()
            # Envia mensaje al siguiente request
            messages.success(request, 'Producto registrado')
        else:
            data['form'] = formulario
    return render(request, 'app/producto/agregar.html', data)


@permission_required('app.view_producto')
def listarProductos(request):
    productos = Producto.objects.all()

    # Para paginar(devuelve variable page si no existe devuelve 1)
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productos, 5)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator
    }

    return render(request, 'app/producto/listar.html', data)


@permission_required('app.change_producto')
def modificarProducto(request, id):

    # Busca un producto donde id=id (Tira una excepcion por eso se utiliza este metodo)
    producto = get_object_or_404(Producto, id=id)

    data = {
        'form': ProductoForms(instance=producto)
    }

    # Si llegan datos por POST
    if(request.method == 'POST'):
        formulario = ProductoForms(
            data=request.POST, files=request.FILES, instance=producto)
        # Si es valido guarda
        if(formulario.is_valid()):
            formulario.save()
            # Envia mensaje al siguiente request
            messages.success(request, 'Modificado correctamente')

            return redirect(to='listar_productos')
        else:
            data['form'] = formulario

    return render(request, 'app/producto/modificar.html', data)


@permission_required('app.delete_producto')
def eliminarProduto(request, id):
    # Busca un producto donde id=id (Tira una excepcion por eso se utiliza este metodo)
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    # Envia mensaje al siguiente request
    messages.success(request, 'Eliminado correctamente')
    return redirect(to='listar_productos')


def registro(request):
    data = {
        'form' : CustomUserCreationForm()
    }

    # Si llegan datos por POST
    if(request.method == 'POST'):
        formulario = CustomUserCreationForm(data = request.POST)

        if(formulario.is_valid()):
            formulario.save()

            user = authenticate(username= formulario.cleaned_data['username'], password = formulario.cleaned_data['password1'])
            login(request, user)
            return redirect(to='home')
        else:
            data['form'] =  formulario

    return render(request, 'registration/registro.html', data)
