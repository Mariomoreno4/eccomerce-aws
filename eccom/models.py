from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    favoritos = models.ManyToManyField('Producto', related_name='usuarios_favoritos')
    edad = models.IntegerField(null=True, blank=True)
    juego_favorito = models.CharField(max_length=255, null=True, blank=True)
    plataforma_favorita = models.CharField(max_length=255, null=True, blank=True)
    lugar_residencia = models.CharField(max_length=255, null=True, blank=True)
    ventas_compradas = models.IntegerField(null=True, blank=True, default=0)
    sexo=models.CharField(max_length=255, null=True, blank=True)
    genero=models.CharField(max_length=255, null=True, blank=True)
    coaventura= models.IntegerField(null=True, blank=True, default=0)
    coplataforma= models.IntegerField(null=True, blank=True, default=0)
    coaccion= models.IntegerField(null=True, blank=True, default=0)
    coestrategia= models.IntegerField(null=True, blank=True, default=0)
    codeportivo= models.IntegerField(null=True, blank=True, default=0)
    coterror= models.IntegerField(null=True, blank=True, default=0)
    corol= models.IntegerField(null=True, blank=True, default=0)
    coxbox= models.IntegerField(null=True, blank=True, default=0)
    coplay= models.IntegerField(null=True, blank=True, default=0)
    conintendo= models.IntegerField(null=True, blank=True, default=0)
    comusicales=models.IntegerField(null=True, blank=True, default=0)
    imagen_perfil = models.ImageField(upload_to='profile_images', blank=True, null=True)


    def __str__(self):
        return self.usuario.username
class producto(models.Model):
    
    nombre= models.CharField(max_length=255)
    platform=models.CharField(max_length=255)
    categoria=models.CharField(max_length=255)
    precio=models.FloatField()
    critic_score=models.FloatField()
    user_score=models.FloatField()
    pic= models.CharField(max_length=255,null=True)
   
    def __str__(self):
        return self.nombre

class favoritos(models.Model):
    nombre= models.CharField(max_length=255)
    platform=models.CharField(max_length=255)
    categoria=models.CharField(max_length=255)
    precio=models.FloatField()
    pic= models.CharField(max_length=255,null=True)
    
    
class ordenes(models.Model):
    usuario = models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    nombre_producto = models.CharField(max_length=100,null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
  
    platform=models.CharField(max_length=255,null=True)
    categoria=models.CharField(max_length=255,null=True)
    precio=models.FloatField(default=0)
    critic_score=models.FloatField(default=0)
    user_score=models.FloatField(default=0)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(producto, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reseña de {self.user.username} para {self.product.nombre}'