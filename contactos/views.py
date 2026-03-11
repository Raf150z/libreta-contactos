from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from .models import Contacto
from .forms import ContactoForm, RegistroUsuarioForm
import csv


def home(request):
    return render(request, 'home.html')


def registrar(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a tu libreta de contactos.')
            return redirect('contactos:lista_contactos')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'registration/registrar.html', {'form': form})


@login_required
def lista_contactos(request):
    contactos_list = Contacto.objects.filter(usuario=request.user)
    
    favoritos = request.GET.get('favoritos')
    if favoritos == 'true':
        contactos_list = contactos_list.filter(favorito=True)
    
    query = request.GET.get('q')
    if query:
        contactos_list = contactos_list.filter(
            Q(nombre__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query) |
            Q(direccion__icontains=query)
        )
    
    total_contactos = Contacto.objects.filter(usuario=request.user).count()
    total_favoritos = Contacto.objects.filter(usuario=request.user, favorito=True).count()
    
    contactos_con_telefono = Contacto.objects.filter(
        usuario=request.user
    ).exclude(
        telefono__isnull=True
    ).exclude(
        telefono__exact=''
    ).count()
    
    contactos_con_email = Contacto.objects.filter(
        usuario=request.user
    ).exclude(
        email__isnull=True
    ).exclude(
        email__exact=''
    ).count()
    
    paginator = Paginator(contactos_list, 10)
    page_number = request.GET.get('page')
    contactos = paginator.get_page(page_number)
    
    context = {
        'contactos': contactos,
        'total_contactos': total_contactos,
        'total_favoritos': total_favoritos,
        'contactos_con_telefono': contactos_con_telefono,
        'contactos_con_email': contactos_con_email,
        'query': query,
    }
    return render(request, 'contactos/lista_contactos.html', context)

@login_required
def detalle_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk, usuario=request.user)
    return render(request, 'contactos/detalle_contacto.html', {'contacto': contacto})

@login_required
def crear_contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST, request.FILES)
        if form.is_valid():
            contacto = form.save(commit=False)
            contacto.usuario = request.user
            contacto.save()
            messages.success(request, f'Contacto "{contacto.nombre}" creado exitosamente.')
            return redirect('contactos:lista_contactos')
    else:
        form = ContactoForm()
    
    return render(request, 'contactos/crear_contacto.html', {'form': form, 'accion': 'Crear'})

@login_required
def editar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ContactoForm(request.POST, request.FILES, instance=contacto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Contacto "{contacto.nombre}" actualizado exitosamente.')
            return redirect('contactos:detalle_contacto', pk=contacto.pk)
    else:
        form = ContactoForm(instance=contacto)
    
    return render(request, 'contactos/crear_contacto.html', {
        'form': form,
        'contacto': contacto,
        'accion': 'Editar'
    })

@login_required
def eliminar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk, usuario=request.user)
    if request.method == 'POST':
        nombre = contacto.nombre
        contacto.delete()
        messages.success(request, f'Contacto "{nombre}" eliminado exitosamente.')
        return redirect('contactos:lista_contactos')
    return render(request, 'contactos/eliminar_contacto.html', {'contacto': contacto})

@login_required
def toggle_favorito(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk, usuario=request.user)
    contacto.favorito = not contacto.favorito
    contacto.save()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'favorito': contacto.favorito})
    messages.success(request, f'Contacto {"agregado a" if contacto.favorito else "eliminado de"} favoritos.')
    return redirect('contactos:lista_contactos')

@login_required
def buscar_contactos(request):
    query = request.GET.get('q', '')
    contactos = Contacto.objects.filter(
        usuario=request.user
    ).filter(
        Q(nombre__icontains=query) |
        Q(telefono__icontains=query) |
        Q(email__icontains=query)
    )[:5]
    data = [{
        'id': c.id,
        'nombre': c.nombre,
        'telefono': c.telefono,
        'email': c.email,
        'favorito': c.favorito
    } for c in contactos]
    return JsonResponse({'contactos': data})

@login_required
def exportar_contactos(request):
    contactos = Contacto.objects.filter(usuario=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="mis_contactos_{request.user.username}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Teléfono', 'Email', 'Dirección', 'Favorito'])
    for contacto in contactos:
        writer.writerow([
            contacto.nombre,
            contacto.telefono or '',
            contacto.email or '',
            contacto.direccion or '',
            'Sí' if contacto.favorito else 'No'
        ])
    return response


@login_required
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Has cerrado sesión exitosamente.')
        return redirect('home')
    return redirect('home')