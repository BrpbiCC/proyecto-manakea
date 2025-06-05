from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroClienteForm, LoginForm, UserUpdateForm
from .models import Usuario, TipoUsuario
from datetime import date

# Vista para la página de inicio pública
def inicio(request):
    return render(request, 'core/inicio.html')

# Vista para el registro de usuarios
def registro(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '¡Su registro fue exitoso! Ahora puede iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroClienteForm()
    return render(request, 'core/registro.html', {'form': form})

# Vista para el inicio de sesión
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                auth_login(request, user)
                messages.success(request, f'¡Bienvenido de nuevo, {user.nombre} {user.apellido}!')
                return redirect('inicioregistrado')
            else:
                messages.error(request, 'Ocurrió un error inesperado al iniciar sesión.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

# Vista para cerrar sesión
def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('inicio')

# Vista para la página de inicio de usuarios registrados
@login_required(login_url='login')
def inicioregistrado(request):
    return render(request, 'core/inicioregistrado.html')

# Vista de perfil actualizada
@login_required(login_url='login')
def perfil(request):
    form_submitted = False # Nueva variable para controlar la visibilidad del formulario
    if request.method == 'POST':
        form_submitted = True # Si es un POST, el formulario ha sido enviado
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado con éxito!')
            return redirect('perfil')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en '{form.fields[field].label}': {error}")
    else:
        form = UserUpdateForm(instance=request.user)
    
    reservas = []
    try:
        reservas = request.user.reserva_set.all().order_by('-fecha_inicio') 

        hoy = date.today()
        for r in reservas:
            if r.fecha_fin and r.fecha_fin < hoy:
                r.estado_display = 'Completado' 
            elif r.estado == 'pendiente':
                r.estado_display = 'Pendiente'
            elif r.estado == 'confirmado':
                r.estado_display = 'Confirmado'
            elif r.estado == 'cancelado':
                r.estado_display = 'Cancelado'
            else:
                r.estado_display = r.estado.capitalize()

    except AttributeError:
        messages.info(request, "No se encontraron reservas o la configuración del modelo de reservas no es correcta.")
        reservas = []
    except Exception as e:
        messages.error(request, f"Error al cargar reservas: {e}")
        reservas = []

    context = {
        'form': form,
        'reservas': reservas,
        'user': request.user,
        'form_submitted': form_submitted, # Pasamos la variable al contexto
    }
    return render(request, 'core/perfil.html', context)

# Resto de tus vistas (puedes protegerlas con @login_required si es necesario)
def hospedaje(request):
    return render (request, 'core/hospedaje.html')

def actividad(request):
    return render (request, 'core/actividad.html')

def gastronomia(request):
    return render (request, 'core/gastronomia.html')

def carrito(request):
    return render (request, 'core/carrito.html')

@login_required
def listar_servicios_anfitrion(request):
    servicios = []
    context = {
        'servicios': servicios,
    }
    return render(request, 'core/listar_servicios_anfitrion.html', context)

@login_required
def listar_reservas_anfitrion(request):
    servicios = []
    context = {
        'servicios': servicios,
    }
    return render(request, 'core/listar_reservas_anfitrion.html', context)