from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
# Create your views here.
from .forms import ReviewForm
from eccom.carrito import Carrito
from eccom.context_processor import total_carrito
from eccom.models import producto
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.db.models import Count


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Obtener los datos adicionales del formulario
            edad = request.POST.get('edad')
            juego_favorito = request.POST.get('juego_favorito')
            plataforma_favorita = request.POST.get('plataforma_favorita')
            lugar_residencia = request.POST.get('lugar_residencia')
            sexo = request.POST.get('sexo')
            genero = request.POST.get('genero')
            # Crear un perfil de usuario con los datos adicionales
            perfil_usuario = PerfilUsuario.objects.create(
                usuario=user,
                edad=edad,
                juego_favorito=juego_favorito,
                plataforma_favorita=plataforma_favorita,
                lugar_residencia=lugar_residencia,
                sexo=sexo,
                genero=genero
            )
            perfil_usuario.save()
            messages.success(request, "El usuario ha sido registrado exitosamente!")
            return render(request, 'registration/login.html')
        else:
            messages.error(request, "No se pudo registrar el usuario, por favor inténtalo de nuevo.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
    
def login(request):
    return render(request,'login.html')
def exit(request):
    logout(request)
    return redirect('/');
def perfil(request):
    usuario = request.user
    # Obtener el perfil del usuario actual
    perfil = PerfilUsuario.objects.get(usuario=usuario)
    ordenes_usuario = ordenes.objects.filter(usuario=usuario)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)
    
    return render(request, 'perfil.html', {"perfil": perfil, "form": form, "ordenes_usuario": ordenes_usuario})
def index(request):
    
    articulos = producto.objects.all()
    paginator = Paginator(articulos, 12)  # Cambia 4 al número deseado de artículos por página
    page = request.GET.get('page')
    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        articulos = paginator.page(1)
    except EmptyPage:
        articulos = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'articulos': articulos})

def todo(request):
    query = request.GET.get('q')
    
    categorias = request.GET.getlist('categoria')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    platforms = request.GET.getlist('platform')

    # Obtener todos los productos
    articulos = producto.objects.all()

    # Filtrar los productos según la consulta de búsqueda
    if query:
        articulos = articulos.filter(Q(nombre__icontains=query) | Q(categoria__in=query) | Q(platform__icontains=query))

    # Filtrar por categorías si están presentes
    if categorias:
        articulos = articulos.filter(categoria__in=categorias)

    # Filtrar por precio si los valores mínimo y máximo están presentes
    if precio_min:
        articulos = articulos.filter(precio__gte=float(precio_min))
    if precio_max:
        articulos = articulos.filter(precio__lte=float(precio_max))

    # Filtrar por plataforma si están presentes
    if platforms:
        articulos = articulos.filter(platform__in=platforms)

    # Paginar los resultados
    paginator = Paginator(articulos, 6)
    page_number = request.GET.get('page')

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    
     

    return render(request, 'todos.html', {'articulos': page, 'query': query,})
def detalle_articulo(request, producto_id):
    
    usuario = request.user
    carrito = Carrito(request)
    articulo = producto.objects.get(id=producto_id)
    reviews = Review.objects.filter(product=articulo)  # Filtrar revisiones por el producto actual

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
         user = request.user
         # Verificar si el usuario ya ha dejado una revisión para este producto
         existing_review = Review.objects.filter(user=user, product=articulo).exists()
         if existing_review:
            # Mostrar un mensaje de error o redirigir con un mensaje indicando que el usuario ya ha revisado este producto
            messages.error(request, "Ya has revisado este producto.")
            return redirect('detalle_articulo', producto_id=producto_id)
        
        rating = form.cleaned_data['rating']
        review_text = form.cleaned_data['review_text']
        review = Review.objects.create(user=user, product=articulo, rating=rating, review_text=review_text)
        # Puedes redirigir a una página diferente después de agregar la reseña si es necesario
        return redirect('detalle_articulo', producto_id=producto_id)
    else:
        form = ReviewForm()
    ratings_count = {
        '5': reviews.filter(rating=5).count(),
        '4': reviews.filter(rating=4).count(),
        '3': reviews.filter(rating=3).count(),
        '2': reviews.filter(rating=2).count(),
        '1': reviews.filter(rating=1).count(),
    }
        
    paginator = Paginator(reviews, 5)  # 10 revisiones por página
    page = request.GET.get('page')

    try:
        paginated_reviews = paginator.page(page)
    except PageNotAnInteger:
        paginated_reviews = paginator.page(1)
    except EmptyPage:
        paginated_reviews = paginator.page(paginator.num_pages)


    return render(request, 'detalle_articulo.html', {'articulo': articulo, 'usuario': usuario, 'form': form, 'reviews': reviews,'ratings_count': ratings_count,'paginated_reviews': paginated_reviews,
})
@login_required
def carrito(request):
    usuario = request.user
    return render(request,'carrito_index.html', {'usuario': usuario});

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
   # `Producto = producto.objects.get(id=producto_id)` is a query in Django that retrieves a single
   # instance of the `producto` model from the database based on the `id` provided in the
   # `producto_id` variable. This line of code is fetching a specific product object with the given
   # `id` for further processing in the view functions.
    Producto = producto.objects.get(id=producto_id)
    carrito.agregar(Producto)
    return redirect("carrito")

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    Producto = producto.objects.get(id=producto_id)
    carrito.eliminar(Producto)
    return redirect("carrito")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    Producto = producto.objects.get(id=producto_id)
    carrito.restar(Producto)
    return redirect("carrito")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("carrito")


def orde(request):
    total_carrito_value = total_carrito(request)
    if request.method == 'POST':
        carrito = Carrito(request)
        if carrito.carrito:  # Verifica si hay elementos en el carrito
            for key, value in carrito.carrito.items():
                plataforma = value['plataforma']
                categoria = value['categoria']
                cantidad = value['cantidad']
                acumulado=value['acumulado']
                nombre_producto = value['nombre']
                if categoria=="Aventura":
                    # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.ventas_compradas is None:
                     perfil_usuario.ventas_compradas = 0  # o cualquier otro valor predeterminado que desees
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                if categoria=="Aventura":
                    # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.coaventura is None:
                     perfil_usuario.coaventura = 0 # o cualquier otro valor predeterminado que desees
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.coaventura += 1
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                if categoria=="Plataforma":
                    # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.coplataforma is None:
                     perfil_usuario.coplataforma = 0  # o cualquier otro valor predeterminado que desees
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.coplataforma += 1
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                if categoria=="Accion":
                    # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.coaccion is None:
                     perfil_usuario.coaccion = 0  # o cualquier otro valor predeterminado que desees
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.coaccion += 1
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                if categoria=="Estrategia":
                    # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.coestrategia is None:
                     perfil_usuario.coestrategia = 0  # o cualquier otro valor predeterminado que desees
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.coestrategia += 1
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                if categoria=="Deportivo":
                    # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.codeportivo is None:
                     perfil_usuario.codeportivo = 0  # o cualquier otro valor predeterminado que desees
                    
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.codeportivo += 1
                    perfil_usuario.ventas_compradas += 1
                   
                    perfil_usuario.save()
                if categoria=="Terror":
                        # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.coterror is None:
                     perfil_usuario.coterror = 0  # o cualquier otro valor predeterminado que desees
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.coterror += 1
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                if categoria=="Rol":
                        # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.corol is None:
                     perfil_usuario.corol = 0  # o cualquier otro valor predeterminado que desees
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.corol += 1
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                if categoria=="Musicales":
                        # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.comusicales is None:
                     perfil_usuario.comusicales = 0  # o cualquier otro valor predeterminado que desees
                     perfil_usuario.ventas_compradas = 0 
                    perfil_usuario.comusicales += 1
                    perfil_usuario.ventas_compradas += 1
                    perfil_usuario.save()
                
                    
                
                if plataforma == "X360":
                    # Aumenta el contador correspondiente en el perfil del usuario
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.coxbox is None:
                     perfil_usuario.coxbox = 0  # o cualquier otro valor predeterminado que desees
                    perfil_usuario.coxbox += 1
                    perfil_usuario.save()
                if plataforma == "PS3" or plataforma == "PSP" or plataforma == "PS4":
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.coplay is None:
                     perfil_usuario.coplay = 0  # o cualquier otro valor predeterminado que desees
                    perfil_usuario.coplay += 1
                    perfil_usuario.save()
                if plataforma == "WII" or plataforma == "3DS" or plataforma == "WIIU":
                    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    if perfil_usuario.conintendo is None:
                     perfil_usuario.conintendo = 0  # o cualquier otro valor predeterminado que desees
                    perfil_usuario.conintendo += 1
                    perfil_usuario.save()
                
                # Crea una instancia del modelo ordenes y guarda la orden en la base de datos
                orden = ordenes.objects.create(
                    usuario=request.user,  # Asocia la orden con el usuario actualmente autenticado
                    cantidad=cantidad,
                    nombre_producto=nombre_producto,
                    platform=plataforma,
                    categoria=categoria,
                    precio=acumulado,  # Aquí debes establecer el precio según lo que corresponda en tu lógica
                   
                )

            # Limpia el carrito después de guardar los elementos en la base de datos
            carrito.limpiar()

            return render(request, 'confirmacion.html')

  
    
    host = request.get_host()
  
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total_carrito_value['total_carrito'],  # Utiliza el total del carrito obtenido
        'invoice': uuid.uuid4(),
        'currency_code': 'MXN',
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'paypal': paypal_payment,
    }
    
    return render(request, 'orde.html', context)
def confirmacion(request):
    return render(request, "confirmacion.html")
@login_required
def favorito(request):
    perfil_usuario = PerfilUsuario.objects.get(usuario=request.user)

    # Obtener la lista de favoritos del usuario
    favoritos_usuario = perfil_usuario.favoritos.all()

    # Renderizar la página de favoritos con los productos favoritos del usuario
    return render(request, 'favoritos.html', {'favoritos_usuario': favoritos_usuario})
@login_required
def agregar_favorito(request, producto_id):
     # Obtener el producto por su ID
    Producto = producto.objects.get(id=producto_id)

    # Obtener o crear el perfil de usuario asociado al usuario actual
    perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user)

    # Agregar el ID del producto a la lista de favoritos del usuario
    perfil_usuario.favoritos.add(producto_id)
    carrito = Carrito(request)
    Producto = producto.objects.get(id=producto_id)
    carrito.agregar(Producto)

    # Redirigir a la página de favoritos o a donde desees
    return redirect('fav')


@login_required
def eliminar_favorito(request, producto_id):
    # Obtener el producto por su ID
    Producto_a_eliminar = producto.objects.get(id=producto_id)

    # Obtener el perfil de usuario asociado al usuario actual
    perfil_usuario = PerfilUsuario.objects.get(usuario=request.user)

    # Eliminar el producto de la lista de favoritos del usuario
    perfil_usuario.favoritos.remove(Producto_a_eliminar)

    # Redirigir a la página de favoritos o a donde desees
    return redirect('fav')



def buscar_productops3(request):
    # Realiza la búsqueda en la base de datos
    articulos = producto.objects.filter(platform='PS3')
    
    
    paginator = Paginator(articulos, 3)
    page = request.GET.get('page')
    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        articulos = paginator.page(1)
    except EmptyPage:
        articulos = paginator.page(paginator.num_pages)
    # Pasa los resultados a la plantilla
    return render(request, 'todos.html', {'articulos': articulos})

def buscar_productowii(request):
    # Realiza la búsqueda en la base de datos
   
    articulos = producto.objects.filter(platform='3DS')
    paginator = Paginator(articulos, 3)
    page = request.GET.get('page')
    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        articulos = paginator.page(1)
    except EmptyPage:
        articulos = paginator.page(paginator.num_pages)
    # Pasa los resultados a la plantilla
    # Pasa los resultados a la plantilla
    return render(request, 'todos.html', {'articulos': articulos})

def buscar_productox360(request):
    # Realiza la búsqueda en la base de datos
    
    articulos = producto.objects.filter(platform='X360')
    
    paginator = Paginator(articulos, 3)
    page = request.GET.get('page')
    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        articulos = paginator.page(1)
    except EmptyPage:
        articulos = paginator.page(paginator.num_pages)
    # Pasa los resultados a la plantilla
    return render(request, 'todos.html', {'articulos': articulos})



def agregar_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            user = request.user
            product_id = request.POST.get('product_id')
            product = get_object_or_404(producto, pk=product_id)
            
            # Verificar si el usuario ya ha dejado una reseña para este producto
            existing_review = Review.objects.filter(user=user, product=product).exists()
            
            if not existing_review:
                rating = form.cleaned_data['rating']
                review_text = form.cleaned_data['review_text']
                review = Review.objects.create(user=user, product=product, rating=rating, review_text=review_text)
                return redirect('detalle_producto', producto_id=product_id)
            else:
                # Usuario ya ha dejado una reseña para este producto
                # Puedes mostrar un mensaje de error o redirigirlos a otra página
                return HttpResponse("Ya has dejado una reseña para este producto.")
    else:
        form = ReviewForm()
    return render(request, 'tu_template.html', {'form': form})
