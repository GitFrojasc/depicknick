from django.db import models
from django.contrib.auth.models import User


class PerfilCliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.get_full_name() or self.usuario.username}"


class DireccionEnvio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='direcciones')
    ciudad = models.CharField(max_length=100)
    direccion = models.TextField()
    veces_usada = models.PositiveIntegerField(default=1)
    ultima_vez = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ciudad} — {self.direccion[:50]}"

    class Meta:
        ordering = ['-ultima_vez']
        verbose_name = "Dirección de envío"
        verbose_name_plural = "Direcciones de envío"


class Productor(models.Model):
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    historia = models.TextField()
    foto = models.ImageField(upload_to='productores/', blank=True)
    video_url = models.URLField(blank=True, help_text="URL del video de YouTube")
    email = models.EmailField(blank=True, help_text="Para notificaciones automáticas de stock agotado")
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Productores"


class Categoria(models.Model):
    TIPOS = [
        ('despensa', 'La Despensa'),
        ('gourmet', 'Soltero Gourmet'),
        ('ancheta', 'Ancheta'),
        ('picknick', 'De Picknick'),
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField(blank=True)
    emoji = models.CharField(max_length=10, default='🧺')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías"


class Producto(models.Model):
    COBERTURA_CHOICES = [('local', 'Solo local'), ('nacional', 'Envío nacional')]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    historia = models.TextField(help_text="La historia detrás de este producto")
    ingredientes = models.TextField(blank=True, help_text="Lista de ingredientes o componentes")
    productor = models.ForeignKey(Productor, on_delete=models.SET_NULL, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio al detal (consumidor final)")
    precio_mayor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Precio al por mayor (restaurantes, revendedores)")
    unidad = models.CharField(max_length=50, default='unidad', help_text="kg, unidad, 250g, etc.")
    unidad_mayor = models.CharField(max_length=50, blank=True, help_text="Ej: caja x 12, bulto x 50kg")
    caducidad = models.CharField(max_length=100, blank=True, help_text="Ej: 6 meses sellado, refrigerado 15 días")
    tiempo_espera = models.PositiveIntegerField(default=0, help_text="Días de espera promedio por pedido")
    cobertura_envio = models.CharField(max_length=10, choices=COBERTURA_CHOICES, default='local', help_text="¿Se puede enviar a todo el país?")
    foto = models.ImageField(upload_to='productos/', blank=True)
    video_url = models.URLField(blank=True, help_text="Video YouTube del producto")
    certificado = models.BooleanField(default=False, help_text="Cumple normas internacionales")
    disponible = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0, help_text="Unidades disponibles en inventario")
    stock_minimo = models.PositiveIntegerField(default=5, help_text="Envía alerta al productor cuando baje de este número")
    creado = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        stock_anterior = None
        if self.pk:
            try:
                stock_anterior = Producto.objects.get(pk=self.pk).stock
            except Producto.DoesNotExist:
                pass

        if self.stock == 0:
            self.disponible = False
        elif self.stock > 0:
            self.disponible = True

        super().save(*args, **kwargs)

        if self.productor and self.productor.email:
            self._notificar_si_necesario(stock_anterior)

    def _notificar_si_necesario(self, stock_anterior):
        from django.core.mail import send_mail
        nombre_prod = self.productor.nombre
        email_prod = self.productor.email

        if stock_anterior != 0 and self.stock == 0:
            send_mail(
                subject=f'[dePicknick] AGOTADO: {self.nombre}',
                message=(
                    f'Hola {nombre_prod},\n\n'
                    f'El producto "{self.nombre}" se ha agotado en dePicknick.\n'
                    f'Por favor contáctanos para coordinar el próximo envío.\n\n'
                    f'Equipo dePicknick\nhola@depicknick.com'
                ),
                from_email='hola@depicknick.com',
                recipient_list=[email_prod],
                fail_silently=True,
            )
        elif stock_anterior is not None and stock_anterior > self.stock_minimo and 0 < self.stock <= self.stock_minimo:
            send_mail(
                subject=f'[dePicknick] Stock bajo: {self.nombre}',
                message=(
                    f'Hola {nombre_prod},\n\n'
                    f'El producto "{self.nombre}" tiene solo {self.stock} unidades restantes.\n'
                    f'Te avisamos para que puedas preparar el próximo lote.\n\n'
                    f'Equipo dePicknick\nhola@depicknick.com'
                ),
                from_email='hola@depicknick.com',
                recipient_list=[email_prod],
                fail_silently=True,
            )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Productos"


class Canasto(models.Model):
    TIPOS = [
        ('despensa', 'La Despensa'),
        ('gourmet', 'Soltero Gourmet'),
        ('ancheta', 'Ancheta'),
        ('picknick', 'De Picknick'),
    ]
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    foto = models.ImageField(upload_to='canastos/', blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_tipo_display()} — {self.nombre}"

    class Meta:
        verbose_name_plural = "Canastos"


class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('preparando', 'Preparando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    METODOS_PAGO = [
        ('stripe', 'Tarjeta / Internacional (Stripe)'),
        ('bold', 'PSE / Nequi / Daviplata (Bold)'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos')
    nombre_cliente = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100)
    direccion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stripe_payment_id = models.CharField(max_length=200, blank=True)
    notas = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.pk} — {self.nombre_cliente}"

    class Meta:
        verbose_name_plural = "Pedidos"
        ordering = ['-creado']


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad}x {self.producto}"


class Suscripcion(models.Model):
    FRECUENCIAS = [
        ('semanal', 'Semanal'),
        ('quincenal', 'Quincenal'),
        ('mensual', 'Mensual'),
    ]

    nombre_cliente = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100)
    direccion = models.TextField()
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIAS, default='semanal')
    activa = models.BooleanField(default=True)

    # Economía circular: seguimiento del material físico en manos del cliente
    tiene_canasto = models.BooleanField(default=False, help_text="El cliente ya tiene el canasto físico")
    tiene_tarro_organicos = models.BooleanField(default=False, help_text="El cliente ya tiene el tarro para desechos orgánicos")

    ultimo_pedido = models.ForeignKey(
        Pedido, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='suscripcion_origen',
        help_text="Pedido anterior — base para repetir la selección"
    )
    proxima_entrega = models.DateField(null=True, blank=True)
    creada = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"Suscripción {self.get_frecuencia_display()} — {self.nombre_cliente}"

    class Meta:
        verbose_name = "Suscripción Despensa"
        verbose_name_plural = "Suscripciones Despensa"
        ordering = ['-creada']
