# Pendientes dePicknick

## 🗄️ Base de datos Railway (PostgreSQL)
1. Canvas Railway → **+ New** → **Database** → **Add PostgreSQL**
2. Cajita del servicio → **Settings** → **Start Command**:
   ```
   python manage.py migrate && gunicorn core.wsgi --log-file -
   ```
3. Una vez migrado, cambiar Start Command a:
   ```
   python manage.py cargar_datos_demo && python manage.py migrate && gunicorn core.wsgi --log-file -
   ```
4. Crear superusuario via Railway Shell:
   ```
   python manage.py createsuperuser
   ```

## 📧 Email Gmail (francopacho79@gmail.com)
1. Ir a myaccount.google.com → Seguridad → Verificación en dos pasos (activar si no está)
2. Bajar a **Contraseñas de aplicaciones** → crear una con nombre `dePicknick`
3. Agregar en Railway → Variables:
   ```
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST_USER=francopacho79@gmail.com
   EMAIL_HOST_PASSWORD=<clave de 16 caracteres>
   ```

## 🌐 Dominio
- Candidato: `vamosdepicnic.com` (por confirmar nombre definitivo)
- Verificar disponibilidad en porkbun.com o namecheap.com (~$12 USD/año)
- Una vez comprado, conectar en Railway → Settings → Networking → Custom Domain
