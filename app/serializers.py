from typing_extensions import Required
from .models import Producto, Marca
from rest_framework import serializers


class MarcaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Marca
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    nombre_marca = serializers.CharField(read_only= True, source= 'marca.nombre')

    # Para poner un serializer dentro de otro
    marca = MarcaSerializer(read_only = True)

    # Para mostrar su relacion y permitir agregar
    marca_id = serializers.PrimaryKeyRelatedField(queryset=Marca.objects.all(), source='marca')

    # Validar
    nombre = serializers.CharField(required=True, min_length = 3)

    # Valida que no se repitan nombres (personalizado)
    def validate_nombre(self, value):
        existe = Producto.objects.filter(nombre = value).exists()

        if(existe):
            raise serializers.ValidationError('Este producto ya existe')
        
        return value

    class Meta:
        model = Producto
        fields = '__all__'
