import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmacia.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def encriptar_contraseñas():
    usuarios = User.objects.all()
    for usuario in usuarios:
        # Verificar si la contraseña ya está encriptada
        if not usuario.password.startswith('pbkdf2_'):
            # Encriptar la contraseña
            usuario.password = make_password(usuario.password)
            # Guardar el usuario con la contraseña encriptada
            usuario.save()

if __name__ == "__main__":
    encriptar_contraseñas()
