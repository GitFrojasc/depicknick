from django.core.management.base import BaseCommand
from tienda.models import Productor, Categoria, Producto


DATOS = [
    {
        'productor': {
            'nombre': 'Doña Rosa Ospina',
            'ubicacion': 'Vereda La Florida, Pereira, Risaralda',
            'historia': 'Rosa lleva 30 años cultivando café de especialidad en las laderas del río Otún. Heredó la finca de su padre y hoy la trabaja con sus dos hijos. Cada cosecha la hace a mano, grano por grano.',
            'video_url': '',
        },
        'productos': [
            {
                'nombre': 'Café Especial Tostado',
                'descripcion': 'Café 100% arábica de altura, tostado artesanalmente en la finca. Notas de panela y frutos rojos.',
                'historia': 'Este café crece a 1.800 metros sobre el nivel del mar en la finca de Doña Rosa. La cosecha es manual y la fermentación dura 36 horas.',
                'precio': 28000,
                'unidad': '250g',
                'tipo_categoria': 'gourmet',
                'destacado': True,
                'certificado': True,
                'stock': 30,
            },
            {
                'nombre': 'Panela Redonda',
                'descripcion': 'Panela pura de caña sin procesar. Dulce natural, sin químicos ni conservantes.',
                'historia': 'Elaborada en el trapiche familiar que Doña Rosa mantiene desde 1995. La caña se cosecha a mano y se procesa el mismo día.',
                'precio': 8500,
                'unidad': '500g',
                'tipo_categoria': 'despensa',
                'destacado': False,
                'certificado': False,
                'stock': 50,
            },
            {
                'nombre': 'Miel de Abejas Nativas',
                'descripcion': 'Miel silvestre recolectada de colmenas naturales en el bosque de la finca. Sin pasteurizar.',
                'historia': 'Las abejas nativas meliponas viven en troncos viejos del bosque. Rosa las cuida desde niña y cada temporada cosecha apenas lo necesario para no dañar la colmena.',
                'precio': 35000,
                'unidad': '350ml',
                'tipo_categoria': 'gourmet',
                'destacado': True,
                'certificado': False,
                'stock': 20,
            },
        ]
    },
    {
        'productor': {
            'nombre': 'Don Hernando Ríos',
            'ubicacion': 'Finca El Paraíso, Montenegro, Quindío',
            'historia': 'Hernando fue agricultor de café toda su vida, pero hace 10 años decidió diversificar y hoy tiene la finca con mayor variedad de frutas tropicales del Quindío. Sus productos llegan frescos cada semana a Pereira y Armenia.',
            'video_url': '',
        },
        'productos': [
            {
                'nombre': 'Mora de Castilla',
                'descripcion': 'Mora fresca cosechada esta semana. Perfecta para jugo, mermelada o consumo directo.',
                'historia': 'Don Hernando siembra mora en curvas de nivel para proteger el suelo. Sin plaguicidas desde hace 5 años — usa control biológico con plantas aromáticas.',
                'precio': 6000,
                'unidad': '500g',
                'tipo_categoria': 'despensa',
                'destacado': True,
                'certificado': False,
                'stock': 40,
            },
            {
                'nombre': 'Aguacate Hass',
                'descripcion': 'Aguacate hass maduro, cremoso, cosechado en el punto exacto. Entrega en 24 horas.',
                'historia': 'Los árboles de aguacate de Don Hernando tienen 8 años — ya en su punto máximo de producción. Cada árbol es podado a mano para garantizar frutos grandes.',
                'precio': 4500,
                'unidad': 'unidad',
                'tipo_categoria': 'despensa',
                'destacado': False,
                'certificado': False,
                'stock': 25,
            },
            {
                'nombre': 'Tomate de Árbol',
                'descripcion': 'Tomate de árbol dulce y jugoso. Ideal para jugos, ensaladas y salsas.',
                'historia': 'Una fruta que casi desaparece del mercado moderno. Don Hernando rescató semillas criollas de sus vecinos mayores y hoy tiene el cultivo más grande de la zona.',
                'precio': 5500,
                'unidad': '1kg',
                'tipo_categoria': 'despensa',
                'destacado': False,
                'certificado': False,
                'stock': 35,
            },
        ]
    },
    {
        'productor': {
            'nombre': 'María Eugenia Cardona',
            'ubicacion': 'Taller artesanal, Chinchiná, Caldas',
            'historia': 'María Eugenia aprendió a hacer conservas con su abuela en Chinchiná. Hoy tiene un taller certificado donde procesa frutas de temporada del Eje Cafetero para convertirlas en productos gourmet de exportación.',
            'video_url': '',
        },
        'productos': [
            {
                'nombre': 'Mermelada de Mora Artesanal',
                'descripcion': 'Mermelada elaborada con mora fresca del Quindío. 70% fruta, sin colorantes ni conservantes artificiales.',
                'historia': 'María Eugenia cocina sus mermeladas en pailas de cobre, igual que su abuela. Cada lote es pequeño — máximo 50 frascos — para garantizar la calidad.',
                'precio': 18000,
                'unidad': '250g',
                'tipo_categoria': 'gourmet',
                'destacado': True,
                'certificado': True,
                'stock': 50,
            },
            {
                'nombre': 'Arequipe de Leche de Búfala',
                'descripcion': 'Arequipe artesanal hecho con leche de búfala del Magdalena Medio. Más cremoso y con sabor profundo.',
                'historia': 'La leche de búfala tiene más grasa que la de vaca, lo que le da al arequipe una textura única. María Eugenia consigue la leche directamente de una familia criadora en La Dorada.',
                'precio': 22000,
                'unidad': '300g',
                'tipo_categoria': 'gourmet',
                'destacado': True,
                'certificado': False,
                'stock': 30,
            },
            {
                'nombre': 'Bocadillo Veleño Premium',
                'descripcion': 'Bocadillo tradicional hecho con guayaba criolla de Vélez. Presentación premium con hoja de bijao.',
                'historia': 'La guayaba veleña tiene un dulzor especial por el clima frío de Santander. María Eugenia la trae directamente de los agricultores de Vélez y la procesa el mismo día de llegada.',
                'precio': 15000,
                'unidad': '200g',
                'tipo_categoria': 'gourmet',
                'destacado': False,
                'certificado': True,
                'stock': 40,
            },
        ]
    },
]


class Command(BaseCommand):
    help = 'Carga 3 productores con 3 productos cada uno como datos de demostración'

    def handle(self, *args, **options):
        categorias = {}
        for tipo, nombre in [('despensa', 'La Despensa'), ('gourmet', 'Soltero Gourmet'), ('ancheta', 'Ancheta'), ('picknick', 'De Picknick')]:
            cat, _ = Categoria.objects.get_or_create(tipo=tipo, defaults={'nombre': nombre, 'emoji': '🧺'})
            categorias[tipo] = cat

        for datos in DATOS:
            productor, creado = Productor.objects.get_or_create(
                nombre=datos['productor']['nombre'],
                defaults=datos['productor']
            )
            accion = 'Creado' if creado else 'Ya existía'
            self.stdout.write(f'{accion}: {productor.nombre}')

            for p in datos['productos']:
                tipo_cat = p.pop('tipo_categoria')
                p['productor'] = productor
                p['categoria'] = categorias[tipo_cat]
                producto, creado = Producto.objects.get_or_create(
                    nombre=p['nombre'],
                    defaults=p
                )
                accion = '  +' if creado else '  ='
                self.stdout.write(f'{accion} {producto.nombre}')

        self.stdout.write(self.style.SUCCESS('\nDatos de demostración cargados correctamente.'))
