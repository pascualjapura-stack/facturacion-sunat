# Sistema de Facturación Electrónica (Perú - SUNAT)

Sistema completo (backend + base de datos + interfaz web) para emitir
comprobantes electrónicos (Factura, Boleta, Notas de Crédito/Débito)
cumpliendo las exigencias de SUNAT, usando un **OSE** (Operador de Servicios
Electrónicos) autorizado como Nubefact o Efact para el envío, firma digital
y obtención del CDR de SUNAT.

## ¿Qué cumple respecto a las exigencias de SUNAT?

- **Numeración por serie y correlativo** único por empresa y tipo de
  comprobante (F001, B001...), sin saltos ni repeticiones.
- **Catálogos oficiales SUNAT** (`app/catalogos.py`): tipo de comprobante
  (01 Factura, 03 Boleta, 07 Nota de Crédito, 08 Nota de Débito), tipo de
  documento de identidad, tipo de afectación del IGV, unidad de medida,
  moneda y motivos de nota de crédito.
- **Cálculo correcto del IGV (18%)** separando operaciones gravadas,
  exoneradas e inafectas (`app/calculos.py`).
- **Emisión electrónica real ante SUNAT** a través de un OSE: se genera el
  XML UBL 2.1, se firma digitalmente y se obtiene el CDR (Constancia de
  Recepción) — todo delegado al OSE mediante su API (`app/ose_client.py`).
- **Trazabilidad**: cada comprobante guarda su estado (`PENDIENTE`,
  `ACEPTADO`, `RECHAZADO`), el hash, y los enlaces al PDF/XML/CDR.
- **Notas de crédito/débito** con referencia al comprobante original y
  motivo (catálogo SUNAT), para anulaciones o correcciones.
- **Multiempresa**: cada empresa emisora tiene su propio RUC, credenciales
  SOL y token del OSE.

## Requisitos previos importantes

1. **RUC activo y afiliado a Facturación Electrónica** en SUNAT (Sistema
   de Emisión Electrónica - SEE, vía OSE).
2. **Contrato con un OSE autorizado** (ej. Nubefact, Efact, BizLinks, etc.)
   — ellos gestionan la firma digital y el envío directo a SUNAT. Este
   sistema ya está integrado con el formato de Nubefact como referencia;
   cambiar de proveedor solo requiere adaptar `app/ose_client.py`.
3. **Certificado digital** vigente (lo gestiona el OSE en la mayoría de
   planes, o lo subes tú si el proveedor lo requiere).

## Instalación

```bash
python3 -m venv venv
source venv/bin/activate    # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

Crea un archivo `.env` (o exporta variables de entorno) con:

```
DATABASE_URL=postgresql+psycopg2://usuario:password@localhost:5432/facturacion
SECRET_KEY=una-clave-secreta-larga-y-aleatoria
OSE_BASE_URL=https://api.nubefact.com/api/v1
```

Si no configuras `DATABASE_URL`, el sistema usa SQLite localmente
(`facturacion.db`) — útil para pruebas, no recomendado en producción.

## Desplegar en internet (para acceder desde PC y Android)

Ver **[DEPLOY.md](./DEPLOY.md)** para la guía paso a paso de despliegue
gratuito en Render, sin necesidad de servidor propio ni dominio.

## Primeros pasos (uso local, en tu propia PC)

```bash
python seed.py          # Crea una empresa demo y un usuario admin
uvicorn app.main:app --reload
```

Abre `http://localhost:8000`, inicia sesión con:
- **Email:** admin@miempresa.com
- **Password:** admin123

Luego:
1. Ve a **Clientes** y registra al menos uno.
2. Ve a **Productos** y registra tu catálogo (con precio de venta que
   incluye IGV).
3. Ve a **Nuevo comprobante**, elige cliente y productos, y emítelo.
   El sistema calculará el IGV, asignará el número correlativo, y lo
   enviará automáticamente a tu OSE para su validación ante SUNAT.

## Configurar tu OSE real

Antes de emitir comprobantes válidos de verdad, entra a la base de datos
(tabla `empresas`) o crea un endpoint de edición y completa:

- `ose_token`: el token/API key que te da tu OSE al contratar el servicio.
- `ose_ruc_proveedor`: normalmente tu propio RUC (según el proveedor).

Mientras `ose_token` esté vacío, los comprobantes se guardan como
`PENDIENTE` pero no se envían a SUNAT (para que puedas probar el sistema
sin arriesgar numeración real).

## Estructura del proyecto

```
sunat_facturacion/
├── app/
│   ├── main.py          # Rutas API + interfaz web (FastAPI)
│   ├── models.py        # Modelos de base de datos (SQLAlchemy)
│   ├── schemas.py        # Validación de datos (Pydantic)
│   ├── crud.py           # Lógica de negocio y numeración
│   ├── calculos.py       # Cálculo de IGV y totales
│   ├── catalogos.py      # Catálogos oficiales SUNAT
│   ├── ose_client.py     # Integración con el OSE (Nubefact/Efact)
│   ├── auth.py           # Autenticación JWT
│   ├── config.py
│   ├── database.py
│   ├── templates/        # Interfaz web (Jinja2)
│   └── static/
├── seed.py               # Datos iniciales
└── requirements.txt
```

## Instalación como app (PWA) en PC y Android

El sistema es una **Progressive Web App (PWA)**: se instala directo desde el
navegador, sin pasar por Play Store ni compilar una app nativa.

**Requisito importante:** para que Chrome permita instalarla, el sitio debe
servirse por **HTTPS** (excepto en `localhost`, donde funciona sin HTTPS
para pruebas). Si lo despliegas en un servidor real, usa un dominio con
certificado SSL (Let's Encrypt, Cloudflare, etc.).

**En Android (Chrome):**
1. Abre la URL del sistema en Chrome.
2. Aparecerá un banner "Instala esta app en tu celular" (o el menú ⋮ →
   "Agregar a pantalla de inicio" / "Instalar app").
3. Se agrega un ícono en la pantalla de inicio y se abre en modo app
   (sin barra de direcciones del navegador).

**En PC (Chrome/Edge):**
1. Abre la URL del sistema.
2. Aparece un ícono de instalación (⊕) en la barra de direcciones, o
   Menú → "Instalar Facturación...".
3. Se abre como una ventana de aplicación independiente.

**Qué se agregó para esto:**
- `app/static/manifest.json` — nombre, ícono, colores de la app.
- `app/static/service-worker.js` — permite el modo "instalable" y cachea
  solo los archivos estáticos (CSS, íconos). **Los datos de facturación
  (clientes, comprobantes, montos) nunca se cachean** — siempre se piden
  al servidor, para no arriesgar mostrar información desactualizada o
  inválida ante SUNAT.
- `app/static/icons/` — íconos de la app (192px y 512px).
- CSS responsivo (`app/static/style.css`) con menú hamburguesa y
  formularios/tablas adaptados a pantallas pequeñas.

**Nota:** la PWA es solo la capa de instalación/UI. El servidor
(`uvicorn`) igual debe estar accesible desde el dispositivo — ya sea en
red local o desplegado en internet (ver sección de despliegue más abajo,
o pídemelo si aún no la tienes).

## Próximos pasos recomendados

- **Anulación / Comunicación de baja** (para el mismo día de emisión) —
  requiere otro endpoint hacia el OSE (`operacion: generar_anulacion`).
- **Guía de Remisión Electrónica** (GRE) si mueves mercadería — es un
  comprobante distinto (catálogo 09) con su propio flujo SUNAT.
- **Resumen diario de boletas** — SUNAT exige un resumen consolidado para
  boletas de venta, que la mayoría de OSE automatizan si les activas la
  opción.
- Cifrar `clave_sol` y `ose_token` en la base de datos (no guardarlos en
  texto plano) antes de pasar a producción.
- Agregar roles y permisos más finos (ej. que "vendedor" no pueda ver
  reportes contables).
