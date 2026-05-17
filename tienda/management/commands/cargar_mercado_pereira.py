from django.core.management.base import BaseCommand
from tienda.models import Mercado, Productor


PRODUCTORES = [
    {
        'nombre': 'Artenatura Vivero',
        'telefono': '3145311247',
        'email': '',
        'ubicacion': 'Colinas del Bosque, Dosquebradas',
        'historia': (
            'Vivero artesanal en Dosquebradas especializado en la propagación de plantas ornamentales '
            'y el diseno de espacios verdes. Ofrecen gran variedad de suculentas, cactus de coleccion, '
            'macetas decorativas, tierra abonada y asesoria personalizada para jardines verticales y terrazas. '
            'En Instagram (@artenatura_vivero10) comparten catalogo de plantas y tips de riego y luz.'
        ),
        'tipo_acuerdo': 'directo',
    },
    {
        'nombre': 'Artesanias El Paisita',
        'telefono': '3137455200',
        'email': '',
        'ubicacion': 'Plaza Minorista La 41, Local 063, Pereira',
        'historia': (
            'Artesano local con tradicion en productos de barro, madera y carbon tipicos del Eje Cafetero. '
            'Elabora jaulas, articulos de barro y fogones de carbon artesanales. Punto fijo en la '
            'Plaza Minorista de Mercado La 41, segundo piso.'
        ),
        'tipo_acuerdo': 'directo',
    },
    {
        'nombre': 'Carbon Son y Sazon',
        'telefono': '3182138283',
        'email': '',
        'ubicacion': 'Pereira',
        'historia': (
            'Emprendimiento gastronomico pereirano enfocado en preparaciones con el toque tradicional '
            'del ahumado y asado al carbon. Atienden pedidos directos via WhatsApp y comparten platos '
            'listos y preparaciones en Instagram (@carbonsonysazon).'
        ),
        'tipo_acuerdo': 'acopio',
    },
    {
        'nombre': 'Makalu Supersazones',
        'telefono': '',
        'email': '',
        'ubicacion': 'Pereira',
        'historia': (
            'Desde 1985 produciendo el autentico sabor familiar en condimentos y saborizadores artesanales. '
            'Casi 40 anos de tradicion pereirana en la cocina colombiana.'
        ),
        'tipo_acuerdo': 'acopio',
    },
    {
        'nombre': 'Gourmet Lab by Pauli Londono',
        'telefono': '3127914638',
        'email': 'gourmetlabpaulilondono@gmail.com',
        'ubicacion': 'Pereira',
        'historia': (
            'Taller creativo de cocina y marca de conservacion artesanal fundada por Pauli Londono en Pereira. '
            'Su enfoque va mas alla del producto: educan a traves de talleres privados, experiencias culinarias '
            'y asesorias gastronomicas. Productos destacados: mermeladas con especias, encurtidos gourmet, '
            'salsas artesanales y conservas vegetales disenadas para tablas de quesos y maridajes. '
            'Instagram: @gourmet.lab_xpauli'
        ),
        'tipo_acuerdo': 'directo',
    },
    {
        'nombre': 'Achiras Huilenses Las Autenticas',
        'telefono': '',
        'email': '',
        'ubicacion': 'Pereira',
        'historia': (
            'Achiras y pasabocas tradicionales elaborados con harina de sagu puro. '
            'Receta ancestral huilense con propiedades benéficas documentadas. '
            'Una de las pocas marcas que mantiene la autenticidad del proceso artesanal.'
        ),
        'tipo_acuerdo': 'acopio',
    },
    {
        'nombre': 'Panaderia Artesanal Masa Madre',
        'telefono': '3194995331',
        'email': '',
        'ubicacion': 'Pereira',
        'historia': (
            'Panaderia artesanal que trabaja exclusivamente con masa madre natural y fermentacion lenta, '
            'usando ingredientes directos del campo. Cada pan es un proceso de al menos 24 horas. '
            'Atiende pedidos anticipados.'
        ),
        'tipo_acuerdo': 'acopio',
    },
    {
        'nombre': 'Anahi Abonos Organicos',
        'telefono': '3002930958',
        'email': 'anahisobonosorganicos@gmail.com',
        'ubicacion': 'Pereira',
        'historia': (
            'Proyecto agroecologico alineado con la sostenibilidad de Risaralda. Fabrican y comercializan '
            'insumos limpios para el agro y la jardineria urbana: compost de alta calidad, humus de lombriz '
            'liquida y solida, enraizadores naturales y sustratos para huertos caseros. '
            'Ofrecen 10% de descuento en sus productos. Instagram: @abonos_anahi'
        ),
        'tipo_acuerdo': 'directo',
    },
    {
        'nombre': 'Raices Vivas',
        'telefono': '3042803056',
        'email': '',
        'ubicacion': 'Pereira',
        'historia': (
            '"Tejer es sembrar memoria." Marca artesanal que elabora piezas de vestir, accesorios y '
            'elementos decorativos rescatando tecnicas de tejido tradicional con fibras naturales. '
            'Cada pieza es unica y lleva historia del campo colombiano. Instagram: @raicesvivasorigen'
        ),
        'tipo_acuerdo': 'directo',
    },
    {
        'nombre': 'La Panto Arte en Hilo',
        'telefono': '3137416062',
        'email': '',
        'ubicacion': 'Pereira',
        'historia': (
            'Arte contemporaneo en hilo: bordados personalizados, ilustraciones textiles y piezas '
            'decorativas unicas hechas a mano. Cada obra es irrepetible. Instagram: @patpant67'
        ),
        'tipo_acuerdo': 'directo',
    },
    {
        'nombre': 'Finca Despertar',
        'telefono': '3188634437',
        'email': '',
        'ubicacion': 'Pereira',
        'historia': (
            'Marca pereirana dedicada a la alimentacion consciente y saludable. Producen alimentos limpios, '
            'libres de quimicos agresivos y procesados artesanalmente: frutos secos, harinas alternativas, '
            'snacks saludables, productos organicos de temporada y alimentos para dietas fitness, veganas '
            'o libres de gluten. Comunidad activa en Facebook e Instagram (@fincadespertarpereira).'
        ),
        'tipo_acuerdo': 'ambos',
    },
    {
        'nombre': 'De La Cuenca Panaderia',
        'telefono': '',
        'email': '',
        'ubicacion': 'La Florida, Pereira',
        'historia': (
            'Panaderia artesanal ubicada en La Florida, corregimiento de Pereira. '
            'Hecha con amor y con ingredientes locales del campo risaraldense.'
        ),
        'tipo_acuerdo': 'acopio',
    },
    {
        'nombre': 'Antojitos del Eje',
        'telefono': '3214622512',
        'email': '',
        'ubicacion': 'Calle 20 N 5-43 Piso 3, Pereira',
        'historia': (
            'Tradicion del Eje Cafetero en pasabocas: achiras, torta de cuca y bizcochos de manteca y cuajada. '
            'Recetas de generaciones, elaboradas artesanalmente. Pedidos y domicilios al 321 462 2512 '
            'o 314 809 6276.'
        ),
        'tipo_acuerdo': 'acopio',
    },
    {
        'nombre': 'Cora Tienda Agroecologica',
        'telefono': '3009091246',
        'email': 'corpocora@gmail.com',
        'ubicacion': 'Calle 22 No 5-41, Pereira',
        'historia': (
            'Tienda vinculada a redes de comercio justo y mercados campesinos locales. Sirve como puente '
            'para que pequenos productores de alta montana comercialicen directamente. Productos: cafes de '
            'origen, miel de abejas pura, hortalizas organicas y derivados lacteos artesanales. '
            'Producto insignia: el Queso Laguna del Otun, elaborado artesanalmente en las montanas del '
            'Parque Nacional Natural Los Nevados.'
        ),
        'tipo_acuerdo': 'ambos',
    },
    {
        'nombre': 'Colibri Floristeria by Susi',
        'telefono': '3167917246',
        'email': '',
        'ubicacion': 'C.C. Exito Ciudad Victoria, Pereira',
        'historia': (
            'Floristeria artesanal con arreglos unicos elaborados con flores de productores locales '
            'de la region cafetera. Punto fijo en el Centro Comercial Exito Ciudad Victoria. '
            'Instagram: @colibribysusi'
        ),
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

        creados, actualizados = 0, 0
        for datos in PRODUCTORES:
            productor, nuevo = Productor.objects.get_or_create(
                nombre=datos['nombre'],
                defaults={'mercado': mercado, 'estado_editorial': 'borrador', 'activo': True}
            )
            productor.mercado = mercado
            productor.ubicacion = datos.get('ubicacion', '') or productor.ubicacion
            productor.historia = datos.get('historia', '') or productor.historia
            productor.email = datos.get('email', '') or productor.email
            productor.telefono = datos.get('telefono', '') or productor.telefono
            productor.tipo_acuerdo = datos.get('tipo_acuerdo', 'acopio')
            productor.save()
            if nuevo:
                creados += 1
                self.stdout.write(self.style.SUCCESS(f'  [+] {productor.nombre}'))
            else:
                actualizados += 1
                self.stdout.write(f'  [~] {productor.nombre} (actualizado)')

        self.stdout.write(self.style.SUCCESS(
            f'\nListo: {creados} creados, {actualizados} actualizados.'
        ))
        self.stdout.write(
            'Siguiente paso: admin > Productores > seleccionar todos > Enviar correo de invitacion'
        )
