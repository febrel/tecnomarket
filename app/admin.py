from django.contrib import admin
from .models import Marca, Producto, Contacto
from .forms import ProductoForms

# Register your models here.


# Para manejar panel de Producto
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'nuevo', 'marca']
    list_editable = ['precio']
    # Para buscar
    search_fields = ['nombre']
    # Para filtrar
    list_filter = ['marca', 'nuevo']
    # Para asignar las vistas en table (solo 5)
    list_per_page = 5
    # Para que utilice las validaciones creadas
    form= ProductoForms


admin.site.register(Marca)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Contacto)
