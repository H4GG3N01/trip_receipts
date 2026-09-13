# Recibos de Viaje

App para generar recibos PDF de tus viajes con Daniel (el chofer), con folio
manual, pensados para adjuntar en tu plataforma de viáticos.

## Qué hace

- Login simple (tú y Daniel, cada uno con su usuario/contraseña).
- Formulario: folio, fecha, origen, destino, costo, forma de pago.
- Genera un PDF con formato de recibo profesional.
- No guarda nada — ni historial de viajes ni el número de folio. Tú lo
  escribes cada vez.

## 1. Sube el proyecto a GitHub

1. Crea un repositorio nuevo en GitHub (puede ser privado), por ejemplo
   `recibos-viajes`.
2. Sube todos los archivos de esta carpeta (`app.py`, `requirements.txt`,
   `Dockerfile`, `render.yaml`, `.env.example`) a ese repositorio. Si no
   tienes git instalado, dentro del repo vacío usa el enlace "uploading an
   existing file" y arrastra los archivos.

## 2. Despliega en Render

1. Entra a https://render.com y crea una cuenta (o inicia sesión).
2. Clic en **New +** → **Blueprint**.
3. Conecta tu cuenta de GitHub y selecciona el repositorio
   `recibos-viajes`. Render detecta `render.yaml` automáticamente.
4. Antes de confirmar, Render te pide llenar las variables marcadas como
   `sync: false`:
   - `CLIENT_NAME`: tu nombre completo (aparece como cliente en el recibo).
   - `PASS_ANTONIO`: la contraseña que quieras para tu usuario.
   - `PASS_DANIEL`: la contraseña que quieras para el usuario de Daniel.
5. Elige el plan **Starter** (evita que la app se "duerma"; el plan
   gratuito también funciona, solo tarda ~30 seg en despertar tras un rato
   sin uso).
6. Dale **Apply** / **Create**. Render construye la imagen y despliega —
   unos 3-5 minutos la primera vez.
7. Al terminar, Render te da una URL tipo
   `https://recibos-viajes.onrender.com`.

## 3. Usar la app

1. Entra a la URL, inicia sesión con usuario `antonio` o `daniel`.
2. Llena folio, fecha, origen, destino, costo y forma de pago. El folio lo
   escribes tú (ej. `0001`, `0002`...) — lleva tú mismo el control del
   consecutivo.
3. Clic en **Generar recibo PDF** y luego **Descargar PDF**.
4. Sube ese PDF a tu plataforma de viáticos como comprobante.

## Notas

- Los datos fijos del chofer (nombre, teléfono, título del servicio) están
  como variables de entorno en `render.yaml` — si algo cambia, se edita ahí
  sin tocar código.
- Cambia las contraseñas de `.env.example` — es solo una plantilla de
  referencia, no la subas con contraseñas reales a un repositorio público.

## Probar localmente (opcional)

```bash
pip install -r requirements.txt
export CLIENT_NAME="Tu Nombre"
export PASS_ANTONIO="1234"
export PASS_DANIEL="1234"
streamlit run app.py
```
