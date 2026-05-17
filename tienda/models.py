from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ── PERFILES ──────────────────────────────────────────────

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


# ── MERCADO ───────────────────────────────────────────────

class Mercado(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    acopiador = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mercados'
    )
    descripcion = models.TextField(blank=True)
    logo = models.ImageField(upload_to='mercados/', blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} — {self.ciudad}"

    class Meta:
        verbose_name_plural = "Mercados"


# ── PRODUCTORES ───────────────────────────────────────────

class Productor(models.Model):
    ESTADOS = [
        ('borrador',    'Borrador'),
        ('en_revision', 'En revisión'),
        ('publicado',   'Publicado'),
        ('destacado',   'Destacado'),
    ]
    ACUERDOS = [
        ('acopio',  'Centro de acopio'),
        ('directo', 'Envío directo'),
        ('ambos',   'Ambos'),
    ]

    mercado          = models.ForeignKey(Mercado, on_delete=models.SET_NULL, null=True, blank=True, related_name='productores')
    nombre           = models.CharField(max_length=200)
    ubicacion        = models.CharField(max_length=200, blank=True)
    historia         = models.TextField(blank=True)
    foto             = models.ImageField(upload_to='productores/', blank=True)
    video_url        = models.URLField(blank=True, help_text="URL del video de YouTube")
    email            = models.EmailField(blank=True, help_text="Para notificaciones automáticas de stock")
    telefono         = models.CharField(max_length=20, blank=True)
    estado_editorial = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    tipo_acuerdo     = models.CharField(max_length=10, choices=ACUERDOS, default='acopio')
    activo           = models.BooleanField(default=True)

    @property
    def puntaje_completitud(self):
        score = 0
        if self.nombre:                              score += 10
        if self.foto:                                score += 20
        if self.historia and len(self.historia) > 50: score += 20
        if self.email:                               score += 10
        if self.telefono:                            score += 10
        if self.video_url:                           score += 25
        if self.ubicacion:                           score += 5
        return score

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Productores"


# ── CATEGORÍAS ────────────────────────────────────────────

class Categoria(models.Model):
    TIPOS = [
        ('despensa',    'La Despensa'),
        ('gourmet',     'Soltero Gourmet'),
        ('ancheta',     'Ancheta'),
        ('picknick',    'De Picknick'),
        ('artesanias',  'Artesanías'),
    ]
    nombre      = models.CharField(max_length=100)
    tipo        = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField(blank=True)
    emoji       = models.CharField(max_length=10, default='🧺')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías"


# ── PRODUCTOS ─────────────────────────────────────────────

class Producto(models.Model):
    COBERTURA = [('local', 'Solo local'), ('nacional', 'Envío nacional')]
    ESTADOS   = [('borrador', 'Borrador'), ('publicado', 'Publicado'), ('destacado', 'Destacado')]

    nombre           = models.CharField(max_length=200)
    descripcion      = models.TextField()
    historia         = models.TextField(blank=True, help_text="La historia detrás de este producto")
    ingredientes     = models.TextField(blank=True)
    sugerencias_uso  = models.TextField(blank=True, help_text="Tips de uso, maridajes, combinaciones sugeridas")
    meses_temporada  = models.JSONField(default=list, blank=True, help_text="Meses de cosecha, ej: [3,4,5] = mar-may")
    fecha_vencimiento = models.DateField(null=True, blank=True, help_text="Fecha de vencimiento del lote actual")

    productor        = models.ForeignKey(Productor, on_delete=models.SET_NULL, null=True, blank=True)
    categoria        = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    precio           = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio al detal")
    precio_mayor     = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Precio al por mayor")
    unidad           = models.CharField(max_length=50, default='unidad')
    unidad_mayor     = models.CharField(max_length=50, blank=True)
    caducidad        = models.CharField(max_length=100, blank=True)
    tiempo_espera    = models.PositiveIntegerField(default=0, help_text="Días de espera promedio")
    cobertura_envio  = models.CharField(max_length=10, choices=COBERTURA, default='local')

    foto             = models.ImageField(upload_to='productos/', blank=True)
    video_url        = models.URLField(blank=True)
    certificado      = models.BooleanField(default=False)
    disponible       = models.BooleanField(default=True)
    destacado        = models.BooleanField(default=False)
    estado_editorial = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    stock            = models.PositiveIntegerField(default=0)
    stock_minimo     = models.PositiveIntegerField(default=5)
    creado           = models.DateTimeField(auto_now_add=True)

    @property
    def dias_para_vencer(self):
        if not self.fecha_vencimiento:
            return None
        return (self.fecha_vencimiento - timezone.now().date()).days

    @property
    def alerta_vencimiento(self):
        dias = self.dias_para_vencer
        if dias is None:    return 'sin_fecha'
        if dias <= 3:       return 'rojo'
        if dias <= 7:       return 'amarillo'
        return 'verde'

    @property
    def descuento_vencimiento(self):
        return {None: 0, 'sin_fecha': 0, 'verde': 0, 'amarillo': 5, 'rojo': 15}.get(self.alerta_vencimiento, 0)

    @property
    def precio_final(self):
        d = self.descuento_vencimiento
        return self.precio * (1 - d / 100) if d else self.precio

    def save(self, *args, **kwargs):
        stock_anterior = None
        if self.pk:
            try:
                stock_anterior = Producto.objects.get(pk=self.pk).stock
            except Producto.DoesNotExist:
                pass
        self.disponible = self.stock > 0
        super().save(*args, **kwargs)
        if self.productor and self.productor.email:
            self._notificar_si_necesario(stock_anterior)

    def _notificar_si_necesario(self, stock_anterior):
        from django.core.mail import send_mail
        nombre_prod = self.productor.nombre
        email_prod  = self.productor.email
        if stock_anterior != 0 and self.stock == 0:
            send_mail(
                subject=f'[dePicknick] AGOTADO: {self.nombre}',
                message=(
                    f'Hola {nombre_prod},\n\n'
                    f'El producto "{self.nombre}" se ha agotado.\n'
                    f'Por favor contáctanos para coordinar el próximo envío.\n\n'
                    f'Equipo dePicknick\nhola@depicknick.com'
                ),
                from_email='dePicknick <onboarding@resend.dev>',
                recipient_list=[email_prod],
                fail_silently=True,
            )
        elif stock_anterior is not None and stock_anterior > self.stock_minimo and 0 < self.stock <= self.stock_minimo:
            send_mail(
                subject=f'[dePicknick] Stock bajo: {self.nombre}',
                message=(
                    f'Hola {nombre_prod},\n\n'
                    f'"{self.nombre}" tiene solo {self.stock} unidades restantes.\n\n'
                    f'Equipo dePicknick\nhola@depicknick.com'
                ),
                from_email='dePicknick <onboarding@resend.dev>',
                recipient_list=[email_prod],
                fail_silently=True,
            )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Productos"


# ── RECETAS ───────────────────────────────────────────────

class Receta(models.Model):
    DIFICULTAD = [('facil', 'Fácil'), ('media', 'Media'), ('dificil', 'Difícil')]

    nombre      = models.CharField(max_length=200)
    descripcion = models.TextField()
    tiempo_prep = models.PositiveIntegerField(default=15, help_text="Minutos de preparación")
    dificultad  = models.CharField(max_length=10, choices=DIFICULTAD, default='facil')
    foto        = models.ImageField(upload_to='recetas/', blank=True)
    video_url   = models.URLField(blank=True)
    activa      = models.BooleanField(default=True)
    creada      = models.DateTimeField(auto_now_add=True)

    @property
    def disponible_ahora(self):
        return all(
            i.producto.stock > 0
            for i in self.ingredientes.filter(opcional=False).select_related('producto')
        )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Recetas"


class IngredienteReceta(models.Model):
    receta   = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='ingredientes')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='recetas')
    cantidad = models.CharField(max_length=50, help_text="Ej: 200g, 1 unidad, al gusto")
    opcional = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre}"

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"


# ── PAQUETES ──────────────────────────────────────────────

class Paquete(models.Model):
    TIPOS = [
        ('semanal',       'Mercado Semanal'),
        ('ancheta',       'Ancheta'),
        ('evento',        'Evento'),
        ('corporativo',   'Corporativo'),
        ('personalizado', 'Personalizado'),
    ]

    nombre     = models.CharField(max_length=200)
    tipo       = models.CharField(max_length=20, choices=TIPOS)
    mercado    = models.ForeignKey(Mercado, on_delete=models.SET_NULL, null=True, blank=True, related_name='paquetes')
    descripcion = models.TextField(blank=True)
    foto       = models.ImageField(upload_to='paquetes/', blank=True)
    activo     = models.BooleanField(default=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text="Null = curado por admin")
    creado     = models.DateTimeField(auto_now_add=True)

    @property
    def precio_total(self):
        return sum(
            i.producto.precio_final * i.cantidad
            for i in self.items.select_related('producto').all()
        )

    def __str__(self):
        return f"{self.get_tipo_display()} — {self.nombre}"

    class Meta:
        verbose_name_plural = "Paquetes"


class ItemPaquete(models.Model):
    paquete  = models.ForeignKey(Paquete, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    opcional = models.BooleanField(default=False, help_text="El cliente puede quitar este item")

    def __str__(self):
        return f"{self.cantidad}× {self.producto.nombre}"


# ── CLIENTES CORPORATIVOS ─────────────────────────────────

class ClienteCorporativo(models.Model):
    nombre_empresa        = models.CharField(max_length=200)
    nit                   = models.CharField(max_length=20, blank=True)
    contacto              = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='empresa')
    mercado               = models.ForeignKey(Mercado, on_delete=models.SET_NULL, null=True, blank=True)
    descuento_porcentaje  = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    limite_credito        = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    activo                = models.BooleanField(default=True)
    creado                = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_empresa

    class Meta:
        verbose_name = "Cliente Corporativo"
        verbose_name_plural = "Clientes Corporativos"


# ── CANASTOS (conservado de v1) ───────────────────────────

class Canasto(models.Model):
    TIPOS = [
        ('despensa', 'La Despensa'),
        ('gourmet',  'Soltero Gourmet'),
        ('ancheta',  'Ancheta'),
        ('picknick', 'De Picknick'),
    ]
    nombre      = models.CharField(max_length=200)
    tipo        = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    foto        = models.ImageField(upload_to='canastos/', blank=True)
    activo      = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_tipo_display()} — {self.nombre}"

    class Meta:
        verbose_name_plural = "Canastos"


# ── PEDIDOS ───────────────────────────────────────────────

class Pedido(models.Model):
    ESTADOS = [
        ('pendiente',   'Pendiente'),
        ('pagado',      'Pagado'),
        ('preparando',  'Preparando'),
        ('enviado',     'Enviado'),
        ('entregado',   'Entregado'),
        ('cancelado',   'Cancelado'),
    ]
    METODOS_PAGO = [
        ('stripe', 'Tarjeta / Internacional (Stripe)'),
        ('bold',   'PSE / Nequi / Daviplata (Bold)'),
    ]

    usuario              = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos')
    cliente_corporativo  = models.ForeignKey(ClienteCorporativo, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_cliente       = models.CharField(max_length=200)
    email                = models.EmailField()
    telefono             = models.CharField(max_length=20)
    ciudad               = models.CharField(max_length=100)
    direccion            = models.TextField()
    estado               = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    metodo_pago          = models.CharField(max_length=20, choices=METODOS_PAGO, blank=True)
    total                = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stripe_payment_id    = models.CharField(max_length=200, blank=True)
    notas                = models.TextField(blank=True)
    creado               = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.pk} — {self.nombre_cliente}"

    class Meta:
        verbose_name_plural = "Pedidos"
        ordering = ['-creado']


class ItemPedido(models.Model):
    pedido          = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto        = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad        = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad}× {self.producto}"


# ── SUSCRIPCIONES ─────────────────────────────────────────

class Suscripcion(models.Model):
    FRECUENCIAS = [
        ('semanal',   'Semanal'),
        ('quincenal', 'Quincenal'),
        ('mensual',   'Mensual'),
    ]

    nombre_cliente       = models.CharField(max_length=200)
    email                = models.EmailField()
    telefono             = models.CharField(max_length=20)
    ciudad               = models.CharField(max_length=100)
    direccion            = models.TextField()
    frecuencia           = models.CharField(max_length=20, choices=FRECUENCIAS, default='semanal')
    activa               = models.BooleanField(default=True)
    tiene_canasto        = models.BooleanField(default=False)
    tiene_tarro_organicos = models.BooleanField(default=False)
    ultimo_pedido        = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True, related_name='suscripcion_origen')
    proxima_entrega      = models.DateField(null=True, blank=True)
    creada               = models.DateTimeField(auto_now_add=True)
    notas                = models.TextField(blank=True)

    def __str__(self):
        return f"Suscripción {self.get_frecuencia_display()} — {self.nombre_cliente}"

    class Meta:
        verbose_name = "Suscripción Despensa"
        verbose_name_plural = "Suscripciones Despensa"
        ordering = ['-creada']


# ── AGENTE IA ─────────────────────────────────────────────

class DocumentoRAG(models.Model):
    TIPOS = [
        ('producto',   'Producto'),
        ('productor',  'Productor'),
        ('receta',     'Receta'),
        ('faq',        'Pregunta Frecuente'),
        ('wiki',       'Artículo Wiki'),
        ('temporada',  'Temporada / Cosecha'),
    ]

    titulo     = models.CharField(max_length=200)
    contenido  = models.TextField()
    tipo       = models.CharField(max_length=20, choices=TIPOS)
    mercado    = models.ForeignKey(Mercado, on_delete=models.SET_NULL, null=True, blank=True, help_text="Vacío = aplica a todos los mercados")
    producto   = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    productor  = models.ForeignKey(Productor, on_delete=models.SET_NULL, null=True, blank=True)
    activo     = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.titulo}"

    class Meta:
        verbose_name = "Documento RAG"
        verbose_name_plural = "Documentos RAG"


class ConversacionAgente(models.Model):
    usuario    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='conversaciones')
    mercado    = models.ForeignKey(Mercado, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    creada     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversación {self.pk} — {self.usuario or 'Anónimo'}"

    class Meta:
        verbose_name = "Conversación"
        verbose_name_plural = "Conversaciones del Agente"
        ordering = ['-creada']


class MensajeAgente(models.Model):
    ROLES = [('user', 'Cliente'), ('assistant', 'Agente')]

    conversacion = models.ForeignKey(ConversacionAgente, on_delete=models.CASCADE, related_name='mensajes')
    rol          = models.CharField(max_length=10, choices=ROLES)
    contenido    = models.TextField()
    creado       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_rol_display()}: {self.contenido[:50]}"

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes del Agente"
        ordering = ['creado']
