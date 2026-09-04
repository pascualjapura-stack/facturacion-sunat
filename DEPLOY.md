# Guía de despliegue en Render (gratis, sin servidor propio)

Render te da un dominio con HTTPS automático (`tuapp.onrender.com`) sin
necesidad de comprar dominio ni administrar un servidor. El plan gratuito
es suficiente para pruebas y uso inicial.

> ⚠️ **Límite del plan gratuito:** el servicio "se duerme" tras ~15 minutos
> sin uso. La primera visita después de eso tarda unos 30-50 segundos en
> responder mientras despierta. Para uso real de una empresa (sin esa
> demora), el plan pagado más económico de Render resuelve esto — pero
> para probar el sistema, incluyendo la instalación como PWA en tu
> celular, el plan gratis funciona perfecto.

## Paso 1: Sube el proyecto a GitHub

1. Crea una cuenta gratis en [github.com](https://github.com) si no tienes.
2. Crea un repositorio nuevo (botón verde "New").
   - Nombre sugerido: `facturacion-sunat`
   - Puede ser público o privado (con privado también funciona en Render).
3. Sube el contenido de esta carpeta (`sunat_facturacion/`) al repositorio.
   La forma más simple sin usar la terminal: en la página del repo, botón
   **"Add file" → "Upload files"**, arrastra todos los archivos y carpetas,
   y confirma ("Commit changes").

## Paso 2: Crea una cuenta en Render

1. Ve a [render.com](https://render.com) y regístrate (puedes usar tu
   cuenta de GitHub para entrar más rápido — recomendado, así Render ya
   tiene acceso a tus repos).

## Paso 3: Despliega con el Blueprint (un clic)

Este proyecto ya incluye un archivo `render.yaml` que le dice a Render
exactamente qué crear: el servicio web y una base de datos PostgreSQL
gratuita, ya conectados entre sí.

1. En el dashboard de Render, clic en **"New +"** → **"Blueprint"**.
2. Selecciona el repositorio `facturacion-sunat` que subiste.
3. Render detecta el `render.yaml` automáticamente y muestra un resumen:
   - Un **Web Service** llamado `facturacion-sunat`
   - Una **Base de datos PostgreSQL** llamada `facturacion-db`
4. Clic en **"Apply"** / **"Create"**.
5. Espera 2-4 minutos mientras Render instala las dependencias y arranca
   el servidor (puedes ver el progreso en tiempo real en los logs).

## Paso 4: Accede al sistema

1. Cuando el estado pase a **"Live"**, Render te muestra la URL, algo como:
   `https://facturacion-sunat.onrender.com`
2. Ábrela. El sistema crea automáticamente, en el primer arranque, una
   empresa demo y un usuario administrador:
   - **Email:** `admin@miempresa.com`
   - **Contraseña:** `admin123`
3. **Inicia sesión y de inmediato:**
   - Ve a **Configuración** → cambia tu contraseña.
   - Completa el **RUC real de tu empresa** y el **token de tu OSE**
     (Nubefact, Efact, etc.) en la misma pantalla de Configuración.
     Sin esto, los comprobantes se guardan como "PENDIENTE" y no se
     envían realmente a SUNAT.

## Paso 5: Instálalo en tu celular Android

1. Abre la URL `https://facturacion-sunat.onrender.com` en Chrome desde
   tu Android.
2. Aparecerá el banner "Instala esta app en tu celular" (o desde el menú
   ⋮ → "Instalar app" / "Agregar a pantalla de inicio").
3. Listo — queda como un ícono en tu pantalla de inicio, funcionando
   como una app.

Como Render ya sirve todo por HTTPS automáticamente, no necesitas
configurar nada adicional para que la instalación como PWA funcione.

## Actualizar el sistema más adelante

Cada vez que subas cambios nuevos al repositorio de GitHub (por ejemplo,
si me pides ajustes y te doy archivos actualizados), Render vuelve a
desplegar automáticamente en unos minutos — no hay que repetir estos pasos.

## Si más adelante quieres tu propio dominio

Render permite conectar un dominio propio (ej. `facturacion.tuempresa.com`)
gratis, desde la pestaña **"Settings" → "Custom Domains"** del servicio,
apuntando un registro CNAME de tu proveedor de dominio hacia la URL que
te dio Render. El HTTPS se sigue gestionando automáticamente.

## Si prefieres evitar que el sistema "se duerma"

Cuando quieras pasar a uso real (sin demoras de arranque), el siguiente
paso natural es subir el plan del **Web Service** (no de la base de
datos) a uno de pago en la misma pestaña de Settings — el resto de la
configuración no cambia.
