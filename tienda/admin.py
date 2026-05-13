from django.contrib import admin
from django.utils.html import format_html
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpResponse
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from .models import Productor, Categoria, Producto, Canasto, Pedido, ItemPedido, Suscripcion


class ProductoResource(resources.ModelResource):
    productor = fields.Field(
        column_name='productor',
        attribute='productor',
        widget=ForeignKeyWidget(Productor, field='nombre')
    )
    categoria = fields.Field(
        column_name='categoria_tipo',
        attribute='categoria',
        widget=ForeignKeyWidget(Categoria, field='tipo')
    )

    class Meta:
        model = Producto
        fields = (
            'id', 'nombre', 'descripcion', 'historia', 'productor',
            'categoria', 'precio', 'unidad', 'stock', 'stock_minimo',
            'destacado', 'certificado',
        )
        export_order = fields
        import_id_fields = ['nombre']


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('subtotal',)


def _contexto_invitacion(productor, request):
    return {
        'productor': productor,
        'productos': Producto.objects.filter(productor=productor).select_related('categoria'),
        'request': request,
    }


@admin.register(Productor)
class ProductorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'email', 'telefono', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'ubicacion', 'email')
    actions = ['enviar_invitacion', 'previsualizar_invitacion']

    @admin.action(description='Enviar correo de invitación a productores seleccionados')
    def enviar_invitacion(self, request, queryset):
        enviados, sin_email = 0, 0
        for productor in queryset:
            if not productor.email:
                sin_email += 1
                continue
            ctx = _contexto_invitacion(productor, request)
            html = render_to_string('emails/invitacion_productor.html', ctx)
            msg = EmailMultiAlternatives(
                subject=f'Tu marca en dePicknick — {productor.nombre}',
                body=f'Hola {productor.nombre}, te presentamos tu perfil en dePicknick.',
                from_email='hola@depicknick.com',
                to=[productor.email],
            )
            msg.attach_alternative(html, 'text/html')
            msg.send(fail_silently=True)
            enviados += 1
        if enviados:
            self.message_user(request, f'{enviados} correo(s) enviado(s) correctamente.')
        if sin_email:
            self.message_user(request, f'{sin_email} productor(es) sin email configurado — no se les envió.', level='warning')

    @admin.action(description='Previsualizar correo (abre en el navegador)')
    def previsualizar_invitacion(self, request, queryset):
        productor = queryset.first()
        ctx = _contexto_invitacion(productor, request)
        html = render_to_string('emails/invitacion_productor.html', ctx)
        return HttpResponse(html)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'emoji')


@admin.register(Producto)
class ProductoAdmin(ImportExportModelAdmin):
    resource_classes = [ProductoResource]
    list_display = ('nombre', 'categoria', 'productor', 'precio', 'unidad', 'indicador_stock', 'stock', 'destacado', 'certificado', 'disponible')
    list_filter = ('categoria', 'disponible', 'destacado', 'certificado', 'productor')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'stock', 'destacado')
    readonly_fields = ('disponible', 'creado')
    fieldsets = (
        ('Información', {
            'fields': ('nombre', 'descripcion', 'historia', 'productor', 'categoria')
        }),
        ('Precio y presentación', {
            'fields': ('precio', 'unidad', 'precio_mayor', 'unidad_mayor', 'foto', 'video_url', 'destacado', 'certificado')
        }),
        ('Inventario', {
            'fields': ('stock', 'stock_minimo', 'disponible'),
            'description': 'El producto se desactiva automáticamente cuando el stock llega a 0. Se notifica al productor.'
        }),
        ('Sistema', {
            'fields': ('creado',),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Stock')
    def indicador_stock(self, obj):
        if obj.stock == 0:
            color, icono = '#e53e3e', '🔴'
        elif obj.stock <= obj.stock_minimo:
            color, icono = '#dd6b20', '🟡'
        else:
            color, icono = '#38a169', '🟢'
        return format_html(
            '<span style="color:{};font-weight:bold;">{} {}</span>',
            color, icono, obj.stock
        )


@admin.register(Canasto)
class CanastoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'precio_base', 'activo')
    list_filter = ('tipo', 'activo')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_cliente', 'ciudad', 'total', 'estado', 'metodo_pago', 'creado')
    list_filter = ('estado', 'metodo_pago', 'ciudad')
    search_fields = ('nombre_cliente', 'email')
    readonly_fields = ('creado', 'stripe_payment_id')
    inlines = [ItemPedidoInline]


@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ('nombre_cliente', 'email', 'telefono', 'ciudad', 'frecuencia', 'tiene_canasto', 'tiene_tarro_organicos', 'proxima_entrega', 'activa')
    list_filter = ('frecuencia', 'activa', 'tiene_canasto', 'tiene_tarro_organicos', 'ciudad')
    search_fields = ('nombre_cliente', 'email', 'telefono')
    list_editable = ('activa', 'tiene_canasto', 'tiene_tarro_organicos', 'proxima_entrega')
    readonly_fields = ('creada',)
    fieldsets = (
        ('Cliente', {
            'fields': ('nombre_cliente', 'email', 'telefono', 'ciudad', 'direccion')
        }),
        ('Suscripción', {
            'fields': ('frecuencia', 'activa', 'proxima_entrega', 'ultimo_pedido', 'notas')
        }),
        ('Economía circular', {
            'fields': ('tiene_canasto', 'tiene_tarro_organicos'),
            'description': 'Registro del material físico que tiene el cliente en su poder'
        }),
        ('Sistema', {
            'fields': ('creada',),
            'classes': ('collapse',)
        }),
    )
