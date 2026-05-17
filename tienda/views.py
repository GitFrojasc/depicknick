from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from urllib.parse import quote
import stripe
from .forms import SuscripcionForm, CheckoutForm
from .models import Producto, Pedido, ItemPedido


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


def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form, 'carrito_count': _carrito_count(request)})


def checkout(request):
    items, total = _carrito_items(request)
    if not items:
        return redirect('ver_carrito')

    if not settings.STRIPE_SECRET_KEY:
        from django.contrib import messages
        messages.warning(request, 'El sistema de pagos está en configuración. Contáctanos por WhatsApp.')
        return redirect('ver_carrito')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            request.session['checkout_data'] = form.cleaned_data
            stripe.api_key = settings.STRIPE_SECRET_KEY
            line_items = [
                {
                    'price_data': {
                        'currency': 'cop',
                        'product_data': {'name': item['producto'].nombre},
                        'unit_amount': int(item['producto'].precio * 100),
                    },
                    'quantity': item['cantidad'],
                }
                for item in items
            ]
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                customer_email=form.cleaned_data['email'],
                success_url=request.build_absolute_uri('/pago/exito/') + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri('/pago/cancelado/'),
            )
            return redirect(session.url)
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'form': form,
        'items': items,
        'total': total,
        'carrito_count': _carrito_count(request),
    })


def pago_exito(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('inicio')

    existing = Pedido.objects.filter(stripe_payment_id=session_id).first()
    if existing:
        whatsapp_url = _whatsapp_url(existing)
        return render(request, 'confirmacion.html', {
            'pedido': existing,
            'carrito_count': 0,
            'whatsapp_url': whatsapp_url,
        })

    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        stripe_session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.StripeError:
        return redirect('inicio')

    if stripe_session.payment_status != 'paid':
        return redirect('inicio')

    checkout_data = request.session.pop('checkout_data', {})
    items, total = _carrito_items(request)

    if not checkout_data or not items:
        return redirect('inicio')

    pedido = Pedido.objects.create(
        nombre_cliente=checkout_data['nombre_cliente'],
        email=checkout_data['email'],
        telefono=checkout_data['telefono'],
        ciudad=checkout_data['ciudad'],
        direccion=checkout_data['direccion'],
        notas=checkout_data.get('notas', ''),
        metodo_pago='stripe',
        estado='pagado',
        total=total,
        stripe_payment_id=session_id,
    )

    for item in items:
        ItemPedido.objects.create(
            pedido=pedido,
            producto=item['producto'],
            cantidad=item['cantidad'],
            precio_unitario=item['producto'].precio,
        )
        prod = item['producto']
        prod.stock = max(0, prod.stock - item['cantidad'])
        prod.save()

    request.session['carrito'] = {}
    _enviar_confirmacion_pedido(pedido)

    return render(request, 'confirmacion.html', {
        'pedido': pedido,
        'carrito_count': 0,
        'whatsapp_url': _whatsapp_url(pedido),
    })


def pago_cancelado(request):
    items, total = _carrito_items(request)
    return render(request, 'carrito.html', {
        'items': items,
        'total': total,
        'carrito_count': _carrito_count(request),
        'pago_cancelado': True,
    })


def _whatsapp_url(pedido):
    numero = settings.WHATSAPP_NUMBER
    if not numero:
        return None
    msg = quote(f'Hola dePicknick 🧺 Acabo de pagar mi pedido #{pedido.pk} por ${pedido.total:,.0f}. ¿Cuándo me lo entregan?')
    return f'https://wa.me/{numero}?text={msg}'


def _enviar_confirmacion_pedido(pedido):
    from django.core.mail import send_mail
    items_list = '\n'.join(
        f'- {it.cantidad}x {it.producto.nombre}: ${it.subtotal:,.0f}'
        for it in pedido.items.select_related('producto').all()
    )
    send_mail(
        subject=f'Pedido #{pedido.pk} confirmado — dePicknick 🧺',
        message=(
            f'Hola {pedido.nombre_cliente},\n\n'
            f'Tu pedido ha sido confirmado. ¡Gracias por apoyar a nuestros productores!\n\n'
            f'{items_list}\n\n'
            f'Total: ${pedido.total:,.0f}\n'
            f'Entrega en: {pedido.direccion}, {pedido.ciudad}\n\n'
            f'Nos pondremos en contacto contigo para coordinar la entrega.\n\n'
            f'Equipo dePicknick\nhola@depicknick.com'
        ),
        from_email='dePicknick <onboarding@resend.dev>',
        recipient_list=[pedido.email],
        fail_silently=True,
    )
