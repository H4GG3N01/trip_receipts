# Recibos de Viaje

App para generar recibos PDF de tus viajes con Daniel (el chofer), con folio
consecutivo, pensados para adjuntar en tu plataforma de viáticos.

## Qué hace

- Login simple (tú y Daniel, cada uno con su usuario/contraseña).
- Formulario: fecha, origen, destino, costo, forma de pago.
- Genera un PDF con formato de recibo profesional, con folio consecutivo
  automático.
- No guarda historial de viajes — solo genera el PDF al momento.

## 1. Cuenta gratuita de Upstash (para que el folio nunca se reinicie)

Render borra el disco de la app cada vez que se hace un nuevo despliegue, así
que el número de folio necesita vivir en otro lado que no se borre. Usamos
Upstash (tiene un plan gratuito más que suficiente para este uso).

1. Entra a https://upstash.com y crea una cuenta gratuita (puedes usar tu
   cuenta de Google/GitHub).
2. Dale clic a **Create Database**.
3. Ponle un nombre (ej. `recibos-folio`), tipo **Regional**, elige la región
   más cercana a ti, y crea la base de datos.
4. Entra a la base de datos recién creada y busca la sección **REST API**.
5. Copia los valores de `UPSTASH_REDIS_REST_URL` y
   `UPSTASH_REDIS_REST_TOKEN` — los vas a necesitar en el paso 3.

## 2. Sube el proyecto a GitHub

1. Crea un repositorio nuevo en GitHub (puede ser privado), por ejemplo
   `recibos-viajes`.
2. Sube todos los archivos de esta carpeta (`app.py`, `requirements.txt`,
   `Dockerfile`, `render.yaml`, `.env.example`) a ese repositorio.
   - Si usas GitHub Desktop o VS Code, simplemente arrastra la carpeta,
     haz commit y push.

## 3. Despliega en Render

1. Entra a https://render.com y crea una cuenta (o inicia sesión).
2. Clic en **New +** → **Blueprint**.
3. Conecta tu cuenta de GitHub y selecciona el repositorio
   `recibos-viajes`. Render va a detectar el archivo `render.yaml`
   automáticamente y proponerte el servicio `recibos-viajes`.
4. Antes de confirmar, Render te va a pedir llenar las variables marcadas
   como `sync: false`. Llénalas así:
   - `CLIENT_NAME`: tu nombre completo (el que debe aparecer como cliente
     en el recibo).
   - `PASS_ANTONIO`: una contraseña para tu usuario.
   - `PASS_DANIEL`: una contraseña para el usuario de Daniel.
   - `UPSTASH_REDIS_REST_URL` y `UPSTASH_REDIS_REST_TOKEN`: los que
     copiaste en el paso 1.
5. Elige el plan **Starter** (el más económico con el que Render garantiza
   que la app no se "duerma"; en el plan gratuito la app se duerme tras
   inactividad y tarda ~30 seg en despertar, lo cual también es aceptable
   si prefieres no pagar).
6. Dale **Apply** / **Create**. Render va a construir la imagen de Docker y
   desplegar la app — tarda unos 3-5 minutos la primera vez.
7. Cuando termine, Render te da una URL tipo
   `https://recibos-viajes.onrender.com`. Esa es tu app.

## 4. Usar la app

1. Entra a la URL, inicia sesión con usuario `antonio` o `daniel` y la
   contraseña que configuraste.
2. Llena fecha, origen, destino, costo y forma de pago.
3. Clic en **Generar recibo PDF** y luego **Descargar PDF**.
4. Sube ese PDF a tu plataforma de viáticos como comprobante.

## Notas

- Los datos fijos del chofer (nombre, teléfono, título del servicio) están
  como variables de entorno en `render.yaml` — si algo cambia, lo editas
  ahí sin tocar código.
- Si en algún momento quieres agregar historial de viajes (para
  reportes internos, por ejemplo), se puede añadir después usando la misma
  base de Upstash o una hoja de cálculo — no es necesario rehacer nada de
  lo ya construido.
- Cambia las contraseñas de `.env.example` — ese archivo es solo una
  plantilla de referencia, no la subas con contraseñas reales a un
  repositorio público.

## Probar localmente (opcional)

```bash
pip install -r requirements.txt
export CLIENT_NAME="Tu Nombre"
export PASS_ANTONIO="1234"
export PASS_DANIEL="1234"
streamlit run app.py
```

Sin las variables de Upstash configuradas, el folio se guarda en un archivo
local (`folio_counter.json`) solo para que puedas probar.
