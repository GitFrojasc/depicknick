from django.contrib import admin
from .models import Productor, Categoria, Producto, Canasto, Pedido, ItemPedido, Suscripcion


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('subtotal',)


@admin.register(Productor)
class ProductorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'ubicacion')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'emoji')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'productor', 'precio', 'unidad', 'disponible', 'destacado', 'certificado')
    list_filter = ('categoria', 'disponible', 'destacado', 'certificado')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('disponible', 'destacado', 'precio')


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
