from django.shortcuts import render, redirect, get_object_or_404
from .forms import SuscripcionForm
from .models import Producto


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
    return render(request, 'index.html', {'form': form, 'suscrito': suscrito})


def canasto_detalle(request, tipo):
    if tipo not in CANASTOS_INFO:
        from django.http import Http404
        raise Http404
    productos = Producto.objects.filter(
        categoria__tipo=tipo, disponible=True
    ).select_related('productor', 'categoria').order_by('-destacado', 'nombre')
    return render(request, 'canasto.html', {
        'canasto': CANASTOS_INFO[tipo],
        'tipo': tipo,
        'productos': productos,
    })
