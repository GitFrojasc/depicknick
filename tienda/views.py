from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import SuscripcionForm
from .models import Producto


def _carrito_count(request):
    return sum(request.session.get('carrito', {}).values())


def _carrito_items(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return [], 0
    productos = Producto.objects.filter(pk__in=carrito.keys()).select_related('productor')
    items = []
    total = 0
    for p in productos:
        cantidad = carrito[str(p.pk)]
        subtotal = p.precio * cantidad
        total += subtotal
        items.append({'producto': p, 'cantidad': cantidad, 'subtotal': subtotal})
    return items, total


CANASTOS_INFO = {
    'despensa': {
        'nombre': 'La Despensa',
        'emoji': '🥬',
        'tag': '♻️ Suscripción periódica',
        'descripcion': 'Frutas, verduras y productos frescos sin procesar. Del campo a tu cocina, cosechados esta semana.',
        'color': 'linear-gradient(135deg, #e8f5e2, #c8e6c0)',
    },
    'gourmet': {
        'nombre': 'Soltero Gourmet',
        'emoji': '🍯',
        'tag': 'Sin cocina',
        'descripcion': 'Procesados de extrema calidad para disfrutar sin preparar. Mermeladas, quesos, conservas, frutos secos.',
        'color': 'linear-gradient(135deg, #fff3e0, #ffe0b2)',
    },
    'ancheta': {
        'nombre': 'Ancheta',
        'emoji': '🎁',
        'tag': 'Para regalar',
        'descripcion': 'Arma tu ancheta arrastrando los productos que quieras. Presentación premium, entrega en toda Colombia.',
        'color': 'linear-gradient(135deg, #fce4ec, #f8bbd0)',
    },
    'picknick': {
        'nombre': 'De Picknick',
        'emoji': '🧺',
        'tag': 'Experiencia',
        'descripcion': 'El canasto físico + una selección especial para tu salida. Para parques, fincas, y momentos que importan.',
        'color': 'linear-gradient(135deg, #e3f2fd, #bbdefb)',
    },
}


def inicio(request):
    if request.method == 'POST':
        form = SuscripcionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/?suscrito=ok#canastos')
        return render(request, 'index.html', {'form': form, 'modal_abierto': True})
    form = SuscripcionForm()
    suscrito = request.GET.get('suscrito') == 'ok'
    return render(request, 'index.html', {
        'form': form,
        'suscrito': suscrito,
        'carrito_count': _carrito_count(request),
    })


def canasto_detalle(request, tipo):
    if tipo not in CANASTOS_INFO:
        from django.http import Http404
        raise Http404
    productos = Producto.objects.filter(
        categoria__tipo=tipo, disponible=True
    ).select_related('productor', 'categoria').order_by('-destacado', 'nombre')
    carrito = request.session.get('carrito', {})
    return render(request, 'canasto.html', {
        'canasto': CANASTOS_INFO[tipo],
        'tipo': tipo,
        'productos': productos,
        'carrito': carrito,
        'carrito_count': _carrito_count(request),
    })


@require_POST
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id, disponible=True)
    carrito = request.session.get('carrito', {})
    key = str(producto_id)
    carrito[key] = carrito.get(key, 0) + 1
    request.session['carrito'] = carrito
    siguiente = request.POST.get('siguiente', '/')
    return redirect(siguiente)


@require_POST
def quitar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    key = str(producto_id)
    if key in carrito:
        if carrito[key] > 1:
            carrito[key] -= 1
        else:
            del carrito[key]
    request.session['carrito'] = carrito
    return redirect('ver_carrito')


def ver_carrito(request):
    items, total = _carrito_items(request)
    return render(request, 'carrito.html', {
        'items': items,
        'total': total,
        'carrito_count': _carrito_count(request),
    })
