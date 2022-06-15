from django.urls import path, include  
from .views import home, contacto, galeria, agregarProducto, listarProductos, modificarProducto, eliminarProduto, registro, ProductoViewSet, MarcaViewSet
from django.contrib.auth.views import LogoutView
from rest_framework import routers

# Para el REST
router = routers.DefaultRouter()
router.register('producto', ProductoViewSet)
router.register('marca', MarcaViewSet )


urlpatterns = [
    path('', home, name='home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('contacto/', contacto, name='contacto'),
    path('galeria/', galeria, name='galeria'),
    path('agregar-producto/', agregarProducto, name='agregar_producto'),
    path('listar-productos/', listarProductos, name='listar_productos'),
    path('modificar-producto/<id>/', modificarProducto, name='modificar_producto'),
    path('eliminar-producto/<id>/', eliminarProduto, name='eliminar_producto'),
    path('registro/', registro, name='registro'),
    # REST
    path('api/', include(router.urls)),

]
