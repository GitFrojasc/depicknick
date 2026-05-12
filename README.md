# dePicknick — Documentación Técnica

E-commerce de productos campesinos del Eje Cafetero, Colombia.

---

## Stack

- **Backend:** Django 6 + Python 3.12
- **Base de datos:** SQLite (dev) → PostgreSQL (prod)
- **Pagos:** Stripe (internacional) + Bold (Colombia)
- **Archivos estáticos:** Whitenoise
- **Hosting:** Railway (próximamente)

---

## Estructura del proyecto

```
depicknick/
├── core/               ← configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tienda/             ← app principal
│   ├── models.py       ← Productor, Producto, Canasto, Pedido
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── templates/          ← HTML templates Django
├── static/             ← CSS, JS, imágenes
├── media/              ← fotos de productos y productores
├── index.html          ← prototipo frontend (standalone)
├── manage.py
└── venv/               ← entorno virtual (no subir a git)
```

---

## Instalación local

```bash
# 1. Activar entorno virtual
.\venv\Scripts\activate          # Windows
source venv/bin/activate         # Mac/Linux

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Migraciones
python manage.py migrate

# 4. Correr servidor
python manage.py runserver
```

---

## Variables de entorno

Crear archivo `.env` en la raíz:

```
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
BOLD_API_KEY=tu-bold-key
```

---

## Panel de administración

`http://127.0.0.1:8000/admin/`

Desde aquí se gestionan: Productores, Productos, Categorías, Canastos y Pedidos.

---

## Modelos principales

| Modelo | Descripción |
|--------|-------------|
| `Productor` | Campesinos con historia y video |
| `Producto` | Con historia, precio, foto y video YouTube |
| `Canasto` | Los 4 tipos de experiencia |
| `Pedido` | Órdenes con estado y método de pago |
| `ItemPedido` | Productos dentro de cada pedido |

---

## Próximos pasos

1. Vistas y URLs de la tienda
2. Templates Django (conectar el frontend HTML)
3. Drag & drop del canasto (JavaScript)
4. Integración Stripe
5. Integración Bold
6. Hosting en Railway
7. Dominio depicknick.com
