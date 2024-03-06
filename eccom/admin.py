from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *

# Register your models here.

class perfilResource(resources.ModelResource):
    
    fields={
        'id'
        'usuario',
        'favoritos',
        'edad',
        'juego_favorito',
        'plataforma_favorita',
        'lugar_residencia',
        'ventas_compradas',
        'sexo',
        'genero'
    }
    class Meta:
        model=PerfilUsuario

class UserAdmin(ImportExportModelAdmin):
    pass       

class LibroResources(resources.ModelResource):
    
    fields={
        'nombre',
        'descripcion',
        'precio',
        'id'
    }
    class Meta:
        model=producto
        
        
        
@admin.register(producto)  
class productos(ImportExportModelAdmin):
    resource_class=LibroResources


@admin.register(PerfilUsuario)  
class PerfilUsuario(ImportExportModelAdmin):
    resource_class=perfilResource

admin.site.unregister(User)  # Desregistras el User original
admin.site.register(User, UserAdmin)  # Registras el User con tu UserAdmin personalizado

admin.site.register(Review)