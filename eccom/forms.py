
from django import forms
from .models import *

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Review
        fields = ['review_text', 'rating']
        
class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['edad', 'juego_favorito', 'plataforma_favorita', 'lugar_residencia', 'ventas_compradas', 'sexo', 'genero']
        widgets = {
            'sexo': forms.Select(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')]),
            'plataforma_favorita': forms.Select(choices=[('Xbox', 'Xbox'), ('PlayStation', 'PlayStation'), ('Nintendo', 'Nintendo')]),
            'genero': forms.Select(choices=[('Plataforma', 'Plataforma'), ('Acción', 'Acción'), ('Estrategia', 'Estrategia'),('Deportivo', 'Deportivo'),('Terror', 'Terror'),('Rol', 'Rol'),('Musicales', 'Musicales')]),
            'edad': forms.NumberInput(attrs={'min': 10, 'max': 100})
        }
        
       