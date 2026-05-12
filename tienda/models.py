from django.db import models


class Productor(models.Model):
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    historia = models.TextField()
    foto = models.ImageField(upload_to='productores/', blank=True)
    video_url = models.URLField(blank=True, help_text="URL del video de YouTube")
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
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    historia = models.TextField(help_text="La historia detrás de este producto")
    productor = models.ForeignKey(Productor, on_delete=models.SET_NULL, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=50, default='unidad', help_text="kg, unidad, 250g, etc.")
    foto = models.ImageField(upload_to='productos/', blank=True)
    video_url = models.URLField(blank=True, help_text="Video YouTube del producto")
    certificado = models.BooleanField(default=False, help_text="Cumple normas internacionales")
    disponible = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)

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
