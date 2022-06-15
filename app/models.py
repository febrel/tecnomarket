from distutils.command.upload import upload
from django.db import models

# Create your models here.


class Marca(models.Model):
    # Varchar
    nombre = models.CharField(max_length=50)

    # Para que retorne el nombre
    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    descripcion = models.TextField()
    nuevo = models.BooleanField()
    # FK y forma de eliminar (CASCADE se eliminaria todo), (PROTEC que no se eliminen)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    fecha_fabricacion = models.DateField()
    # Para imagenes
    imagen = models.ImageField(upload_to='productos', null=True)

    # Para que retorne el nombre
    def __str__(self):
        return self.nombre


opciones_consulta = [
    [0, 'consulta'],
    [1, 'reclamo'],
    [2, 'sugerencia'],
    [3, 'felicitaciones']
]


class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consulta)
    mensaje = models.TextField()
    avisos = models.BooleanField()

    # Para que retorne el nombre
    def __str__(self):
        return self.nombre
