# dePicknick — Documentación Técnica

E-commerce de productos campesinos del Eje Cafetero, Colombia.
Conecta productores con consumidores urbanos a través de cuatro experiencias: La Despensa, Soltero Gourmet, Ancheta y De Picknick.

- **Repositorio:** https://github.com/GitFrojasc/depicknick
- **Producción:** https://web-production-719bd.up.railway.app
- **Admin:** `/admin/` — usuario: `francisco`

---

## Stack

| Capa | Tecnología |
|------|-----------|
| Backend | Django 6 + Python 3.12 |
| Base de datos | SQLite (dev) → PostgreSQL Railway (prod) |
| Archivos estáticos | Whitenoise |
| Pagos | Stripe (tarjeta/internacional) + Bold (PSE/Nequi/Daviplata) |
| Hosting | Railway |
| Email | Gmail SMTP con app password |

---

## Estructura del proyecto

```
depicknick/
├── core/
│   ├── settings.py          ← config completa (env vars, email, stripe, bold)
│   ├── urls.py              ← rutas principales
│   └── wsgi.py
├── tienda/
│   ├── models.py            ← Productor, Categoria, Producto, Canasto, Pedido, ItemPedido, Suscripcion
│   ├── views.py             ← inicio, canasto_detalle, carrito (agregar/quitar/ver)
│   ├── forms.py             ← SuscripcionForm
│   ├── admin.py             ← admin con import/export, semáforo stock, email productores
│   └── management/commands/
│       └── cargar_datos_demo.py   ← 3 productores + 9 productos del Eje Cafetero
├── templates/
│   ├── index.html           ← homepage: hero, 4 canastos, modal suscripción
│   ├── canasto.html         ← productos por canasto con carrito
│   ├── carrito.html         ← resumen del pedido con totales
│   └── emails/
│       └── invitacion_productor.html   ← email HTML para productores
├── index.html               ← prototipo standalone (no Django, referencia visual)
├── manage.py
├── requirements.txt
├── Procfile                 ← gunicorn para Railway
└── runtime.txt              ← python-3.12.x
```

---

## Instalación local

```bash
# Windows — usar python del venv directamente
venv\Scripts\python.exe manage.py migrate
venv\Scripts\python.exe manage.py cargar_datos_demo
venv\Scripts\python.exe manage.py createsuperuser
venv\Scripts\python.exe manage.py runserver
```

```bash
# Mac/Linux
source venv/bin/activate
python manage.py migrate
python manage.py cargar_datos_demo
python manage.py createsuperuser
python manage.py runserver
```

El sitio queda disponible en `http://127.0.0.1:8000/`

---

## Tutorial: recorrido por la página

### 1. Homepage — `/`

**Secciones:**
- **Hero** — titular y dos botones: "Arma tu canasto" y "Conoce los productores"
- **Los 4 canastos** — tarjetas con link directo a cada tipo
- **La Despensa** — tarjeta especial con detalle del ciclo circular (entrega → recoge canasto anterior → recoge tarro orgánicos → abono al productor)
- **Cómo funciona** — 4 pasos ilustrados
- **Cobertura** — ciudades donde se entrega
- **Modal de suscripción** — se abre al hacer clic en "Suscribirme". Captura: nombre, email, teléfono, ciudad, dirección, frecuencia. Guarda en la tabla `Suscripcion`.

**Contexto que recibe la vista:**
```python
{'form': SuscripcionForm, 'suscrito': bool, 'carrito_count': int, 'modal_abierto': bool}
```

---

### 2. Canasto individual — `/canasto/<tipo>/`

Tipos válidos: `despensa`, `gourmet`, `ancheta`, `picknick`

**Qué muestra:**
- Encabezado con emoji, nombre y descripción del canasto
- Grid de productos disponibles (`disponible=True`) filtrados por categoría
- Cada tarjeta muestra: foto/emoji, nombre, descripción, historia (truncada a 20 palabras), precio, unidad, productor
- Badges: **Destacado** (terracota) y **Certificado** (verde)
- Botón **+ Agregar al canasto** — hace POST a `/carrito/agregar/<id>/` y vuelve a la misma página
- Si el producto ya está en el carrito, el botón cambia a color terracota con ✓

**Contexto:**
```python
{
  'canasto': {'nombre', 'emoji', 'tag', 'descripcion', 'color'},
  'tipo': str,
  'productos': QuerySet[Producto],
  'carrito': dict,           # {str(producto_id): cantidad}
  'carrito_count': int
}
```

---

### 3. Carrito — `/carrito/`

**Qué muestra:**
- Lista de items con emoji de categoría, nombre del producto, productor, precio unitario
- Controles `−` y `+` para cada item (formularios POST)
- Resumen con subtotales por item y total general
- Botón de pago (deshabilitado — *próximamente*)
- Link "Seguir explorando"

**Si el carrito está vacío:** mensaje y botón para volver a los canastos.

**Contexto:**
```python
{'items': [{'producto', 'cantidad', 'subtotal'}], 'total': Decimal, 'carrito_count': int}
```

**Cómo funciona el carrito (sesión):**
El carrito se guarda en `request.session['carrito']` como un diccionario `{str(producto_id): cantidad}`. No requiere login.

---

## Modelos

### `Productor`
| Campo | Tipo | Notas |
|-------|------|-------|
| nombre | CharField | |
| ubicacion | CharField | |
| historia | TextField | |
| foto | ImageField | upload_to='productores/' |
| video_url | URLField | YouTube |
| email | EmailField | Para notificaciones automáticas |
| telefono | CharField | |
| activo | BooleanField | default=True |

### `Categoria`
Tipos: `despensa`, `gourmet`, `ancheta`, `picknick`

### `Producto`
| Campo | Tipo | Notas |
|-------|------|-------|
| precio | DecimalField | Precio al detal |
| precio_mayor | DecimalField | Para restaurantes/revendedores |
| unidad / unidad_mayor | CharField | ej: kg, caja x 12 |
| stock | PositiveIntegerField | Unidades en inventario |
| stock_minimo | PositiveIntegerField | Umbral de alerta (default 5) |
| disponible | BooleanField | **Auto-calculado** por el método `save()` |
| destacado | BooleanField | Aparece primero en el grid |
| certificado | BooleanField | Normas internacionales |

**Lógica automática en `Producto.save()`:**
- Si `stock == 0` → `disponible = False`
- Si `stock > 0` → `disponible = True`
- Si el stock **cayó a 0** desde un valor > 0 → envía email al productor: "AGOTADO"
- Si el stock **cruzó `stock_minimo`** hacia abajo → envía email: "Stock bajo"

### `Suscripcion`
| Campo | Tipo | Notas |
|-------|------|-------|
| frecuencia | CharField | semanal / quincenal / mensual |
| tiene_canasto | BooleanField | El cliente ya tiene el canasto físico |
| tiene_tarro_organicos | BooleanField | El cliente tiene el tarro de orgánicos |
| ultimo_pedido | ForeignKey(Pedido) | Base para repetir la selección |
| proxima_entrega | DateField | |

### `Pedido` + `ItemPedido`
Estados: `pendiente → pagado → preparando → enviado → entregado → cancelado`
Métodos de pago: `stripe`, `bold`

---

## Admin

Acceder en `/admin/` con las credenciales del superusuario.

### Producto — funciones especiales

**Semáforo de stock** — columna visual en la lista:
- 🟢 Stock normal (> stock_minimo)
- 🟡 Stock bajo (≤ stock_minimo, > 0)
- 🔴 Agotado (stock = 0)

**Campos editables en la lista:** precio, stock, destacado (sin abrir el formulario)

**Importar / Exportar Excel** — botones en la parte superior del listado de Productos. Formato de columnas:
```
id, nombre, descripcion, historia, productor, categoria_tipo, precio, unidad, stock, stock_minimo, destacado, certificado
```

### Productor — acciones

**"Enviar correo de invitación"** — selecciona uno o más productores → envía email HTML con su nombre de marca, lista de productos, precios detal y mayor, e inventario actual.

**"Previsualizar correo"** — abre el HTML del email en el navegador antes de enviarlo.

### Suscripcion — campos editables en lista
`activa`, `tiene_canasto`, `tiene_tarro_organicos`, `proxima_entrega`

---

## Comando de datos demo

```bash
python manage.py cargar_datos_demo
```

Carga:
- **3 productores** del Eje Cafetero con email y teléfono
- **9 productos reales** con historia, precio, stock y categorías variadas
- Categorías de los 4 tipos de canasto

Seguro de ejecutar varias veces — usa `get_or_create` para no duplicar.

---

## Variables de entorno

En Railway → Variables. En local, export directo o archivo `.env`:

```
SECRET_KEY=django-insecure-...
DEBUG=False
ALLOWED_HOSTS=web-production-719bd.up.railway.app
DATABASE_URL=postgresql://...        ← lo genera Railway automáticamente

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=francopacho79@gmail.com
EMAIL_HOST_PASSWORD=<app password de 16 caracteres>

STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
BOLD_API_KEY=...
```

---

## Deploy en Railway

### Primera vez (pendiente)

1. En Railway canvas → **+ New → Database → Add PostgreSQL**
2. En el servicio web → **Settings → Start Command:**
   ```
   python manage.py migrate && gunicorn core.wsgi --log-file -
   ```
3. Una vez migrado, cambiar Start Command a:
   ```
   python manage.py cargar_datos_demo && python manage.py migrate && gunicorn core.wsgi --log-file -
   ```
4. Crear superusuario en Railway Shell:
   ```
   python manage.py createsuperuser
   ```
5. Volver el Start Command al de solo migrate+gunicorn.

### Email Gmail

1. `myaccount.google.com` → Seguridad → Verificación en dos pasos (activar)
2. Contraseñas de aplicaciones → crear con nombre `dePicknick`
3. Agregar `EMAIL_BACKEND`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` como variables en Railway

### Dominio

- Candidato: `vamosdepicnic.com` (~$12 USD/año en porkbun.com o namecheap.com)
- Una vez comprado: Railway → Settings → Networking → Custom Domain

---

## Pendientes

Ver [PENDIENTES.md](PENDIENTES.md) para los pasos concretos del deploy.

| Item | Estado |
|------|--------|
| PostgreSQL en Railway | Pendiente |
| Email Gmail | Pendiente |
| Dominio | En evaluación |
| Integración Stripe | Pendiente |
| Integración Bold | Pendiente |
| Drag & drop ancheta | Pendiente |
| Fotos reales de productos | Pendiente |
