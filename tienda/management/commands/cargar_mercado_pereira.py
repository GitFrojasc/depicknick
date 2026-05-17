from django.core.management.base import BaseCommand
from tienda.models import Mercado, Productor


PRODUCTORES = [
    {
        'nombre': 'Artenatura Vivero',
        'categoria': 'Plantas, suculentas, abonos y tierra',
        'telefono': '3145311247',
        'email': '',
        'ubicacion': 'Colinas del Bosque, Dosquebradas',
        'historia': 'Vivero local especializado en plantas ornamentales, suculentas, abonos y tierra para jardín.',
        'tipo_acuerdo': 'directo',
    },
    {
        'nombre': 'Artesanías El Paisita',
        'categoria': 'Jaulas, artículos de barro, fogones de carbón',
        'telefono': '3137455200',
        'email': '',
        'ubicacion': 'Plaza Minorista La 41, Local 063, Pereira',
        'historia': 'Artesano local con tradición en productos de barro y madera típicos del Eje Cafetero.',
        'tipo_acuerdo': 'directo',
    },
    {
        'nombre': 'Carbón Son y Sazón',
        'categoria': 'Alimentos y preparaciones',
        'telefono': '3182138283',
        'email': '',
        'ubicacion': 'Pereira',
        'historia': 'Emprendimiento gastronómico pereirano con presencia en el mercado campesino.',
        'tipo_acuerdo': 'acopio',
    },
    {
        'nombre': 'Makalu Supersazones',
        'categoria': 'Saborizadores y condimentos',
        'telefono': '',
        'email': '',
        'ubicacion': 'Pereira',
        'historia': 'Desde 1985 produciendo el auténtico sabor familiar en condimentos y saborizadores artesanales.',
        'tipo_acuerdo': 'acopio',
    },
    {
        'nombre': 'Gourmet Lab by Pauli Londoño',
        'categoria': 'Conservas artesanales y talleres de cocina',
        'telefono': '3127914638',
        'email': 'gourmetlabpaulilondono@gmail.com',
        'ubicacion': 'Pereira',
        'historia': 'Conservas artesanales elaboradas con productos locales del Eje Cafetero. También ofrece talleres de cocina y catas de café.',
        'tipo_acuerdo': 'directo',
    },
    {
        'nombre': 'Achiras Huilenses — Las Auténticas',
        'categoria': 'Harina de sagú, achiras y pasabocas tradicionales',
        'telefono': '',
        'email': '',
        'ubicacion': 'Pereira',
        'historia': 'Achiras y pasabocas tradicionales elaborados con harina de sagú puro. Receta ancestral huilense con propiedades benéficas.',
        'tipo_acuerdo': 'acopio',
    },
    {
        'nombre': 'Panadería Artesanal Masa Madre',
        'categoria': 'Panes con masa madre natural y fermentación lenta',
        'telefono': '3194995331',
        'email': '',
        'ubicacion': 'Pereira',
        'historia': 'Panadería artesanal que trabaja con masa madre natural y fermentación lenta, usando ingredientes directos del campo.',
        'tipo_acuerdo': 'acopio',
    },
    {
        'nombre': 'Anahí Abonos Orgánicos',
        'categoria': 'Abonos orgánicos y bioinsumos',
        'telefono': '3002930958',
        'email': 'anahisobonosorganicos@gmail.com',
        'ubicacion': 'Pereira',
        'historia': 'Productora de abonos orgánicos y bioinsumos para agricultura limpia. Apoya la transición agroecológica en el campo pereirano.',
        'tipo_acuerdo': 'directo',
    },
    {
        'nombre': 'Raíces Vivas',
        'categoria': 'Tejidos y artesanías',
        'telefono': '3042803056',
        'email': '',
        'ubicacion': 'Pereira',
        'historia': '"Tejer es sembrar memoria." Artesanías en tejido que preservan las tradiciones culturales del campo colombiano.',
        'tipo_acuerdo': 'directo',
    },
    {
        'nombre': 'La Panto — Arte en Hilo',
        'categoria': 'Arte hecho en hilo',
        'telefono': '3137416062',
        'email': '',
        'ubicacion': 'Pereira',
        'historia': 'Artesana especializada en arte hecho en hilo, piezas únicas con técnicas tradicionales del Eje Cafetero.',
        'tipo_acuerdo': 'directo',
    },
    {
        'nombre': 'Finca Despertar',
        'categoria': 'Alimentos saludables',
        'telefono': '3188634437',
        'email': '',
        'ubicacion': 'Pereira',
        'historia': 'Finca agroecológica en Pereira productora de alimentos saludables cultivados con amor y sin agroquímicos.',
        'tipo_acuerdo': 'ambos',
    },
    {
        'nombre': 'De La Cuenca Panadería',
        'categoria': 'Panadería artesanal',
        'telefono': '',
        'email': '',
        'ubicacion': 'La Florida, Pereira',
        'historia': 'Panadería artesanal ubicada en La Florida, corregimiento de Pereira, hecha con amor y con ingredientes locales.',
        'tipo_acuerdo': 'acopio',
    },
    {
        'nombre': 'Antojitos del Eje',
        'categoria': 'Achiras, torta de cuca, bizcocho de manteca y cuajada',
        'telefono': '3214622512',
        'email': '',
        'ubicacion': 'Calle 20 N° 5-43 Piso 3, Pereira',
        'historia': 'Tradición del Eje Cafetero en pasabocas: achiras, torta de cuca y bizcochos de cuajada. Pedidos y domicilios.',
        'tipo_acuerdo': 'acopio',
    },
    {
        'nombre': 'Cora Tienda Agroecológica',
        'categoria': 'Productos agroecológicos — Queso Laguna del Otún',
        'telefono': '3009091246',
        'email': 'corpocora@gmail.com',
        'ubicacion': 'Calle 22 No 5-41, Pereira',
        'historia': 'Tienda agroecológica con productos directos del campo. Distribuye el famoso Queso artesanal Laguna del Otún, producido en las montañas del Parque Nacional.',
        'tipo_acuerdo': 'ambos',
    },
    {
        'nombre': 'Colibrí Floristería by Susi',
        'categoria': 'Flores y arreglos florales',
        'telefono': '3167917246',
        'email': '',
        'ubicacion': 'C.C. Éxito Ciudad Victoria, Pereira',
        'historia': 'Floristería artesanal con arreglos únicos elaborados con flores de productores locales de la región cafetera.',
        'tipo_acuerdo': 'directo',
    },
]


class Command(BaseCommand):
    help = 'Carga el Mercado Pereira de Cosecha y sus productores iniciales'

    def handle(self, *args, **options):
        mercado, created = Mercado.objects.get_or_create(
            nombre='Pereira de Cosecha',
            defaults={
                'ciudad': 'Pereira',
                'descripcion': (
                    'Mercado campesino institucional de la Alcaldía de Pereira. '
                    'Plaza de Bolívar, primer viernes de cada mes. '
                    '50-60 productores de los corregimientos y veredas de Risaralda. '
                    'Venta directa sin intermediarios.'
                ),
                'activo': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'[OK] Mercado creado: {mercado}'))
        else:
            self.stdout.write(f'  Mercado ya existia: {mercado}')

        creados, existentes = 0, 0
        for datos in PRODUCTORES:
            productor, nuevo = Productor.objects.get_or_create(
                nombre=datos['nombre'],
                defaults={
                    'mercado': mercado,
                    'ubicacion': datos.get('ubicacion', ''),
                    'historia': datos.get('historia', ''),
                    'email': datos.get('email', ''),
                    'telefono': datos.get('telefono', ''),
                    'tipo_acuerdo': datos.get('tipo_acuerdo', 'acopio'),
                    'estado_editorial': 'borrador',
                    'activo': True,
                }
            )
            if nuevo:
                creados += 1
                self.stdout.write(self.style.SUCCESS(f'  [+] {productor.nombre}'))
            else:
                existentes += 1
                self.stdout.write(f'  [-] {productor.nombre} (ya existia)')

        self.stdout.write(self.style.SUCCESS(
            f'\nListo: {creados} productores creados, {existentes} ya existian.'
        ))
        self.stdout.write(
            'Siguiente paso: admin > Productores > seleccionar todos > Enviar correo de invitacion'
        )
