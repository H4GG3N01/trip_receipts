import io
import os
import datetime

import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)

# ---------------------------------------------------------------------------
# CONFIGURACIÓN (todo viene de variables de entorno para no tocar el código
# cada vez que algo cambie)
# ---------------------------------------------------------------------------

SERVICE_TITLE = os.environ.get("SERVICE_TITLE", "Servicio de Transporte Ejecutivo")
DRIVER_NAME = os.environ.get("DRIVER_NAME", "Daniel Perez Luna")
DRIVER_PHONE = os.environ.get("DRIVER_PHONE", "7202229307")
CLIENT_NAME = os.environ.get("CLIENT_NAME", "")  # llénalo en Render con tu nombre completo

# Usuarios permitidos: usuario -> password (ambos vienen de variables de entorno)
AUTH_USERS = {
    "antonio": os.environ.get("PASS_ANTONIO", ""),
    "daniel": os.environ.get("PASS_DANIEL", ""),
}

# ---------------------------------------------------------------------------
# GENERACIÓN DEL PDF
# ---------------------------------------------------------------------------

def build_pdf(folio: str, fecha, origen: str, destino: str, costo: float, forma_pago: str) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=25 * mm,
        bottomMargin=25 * mm,
        leftMargin=25 * mm,
        rightMargin=25 * mm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontSize=18,
        textColor=colors.HexColor("#1a1a1a"),
        spaceAfter=2,
    )
    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#555555"),
    )
    folio_style = ParagraphStyle(
        "FolioStyle",
        parent=styles["Normal"],
        fontSize=11,
        alignment=2,  # derecha
        textColor=colors.HexColor("#1a1a1a"),
    )
    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading3"],
        fontSize=11,
        textColor=colors.HexColor("#1a1a1a"),
        spaceBefore=10,
        spaceAfter=6,
    )
    footer_style = ParagraphStyle(
        "FooterStyle",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.HexColor("#888888"),
    )

    elements = []

    # Encabezado: título + folio
    header_table = Table(
        [
            [
                Paragraph(SERVICE_TITLE, title_style),
                Paragraph(f"Folio No. {folio}", folio_style),
            ]
        ],
        colWidths=[110 * mm, 55 * mm],
    )
    header_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(header_table)
    elements.append(Paragraph(f"Chofer: {DRIVER_NAME} &nbsp;&nbsp;|&nbsp;&nbsp; Tel: {DRIVER_PHONE}", subtitle_style))
    elements.append(Spacer(1, 4 * mm))

    # Línea divisoria
    line_table = Table([[""]], colWidths=[165 * mm], rowHeights=[0.6])
    line_table.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.75, colors.HexColor("#cccccc"))]))
    elements.append(line_table)
    elements.append(Spacer(1, 6 * mm))

    elements.append(Paragraph("RECIBO DE VIAJE", section_style))

    fecha_str = fecha.strftime("%d/%m/%Y")
    costo_str = f"${costo:,.2f} MXN"

    data_table = Table(
        [
            ["Cliente:", CLIENT_NAME or "—"],
            ["Fecha del viaje:", fecha_str],
            ["Origen:", origen],
            ["Destino:", destino],
            ["Forma de pago:", forma_pago],
        ],
        colWidths=[45 * mm, 120 * mm],
    )
    data_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.HexColor("#eeeeee")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1a1a1a")),
            ]
        )
    )
    elements.append(data_table)
    elements.append(Spacer(1, 8 * mm))

    # Total
    total_table = Table(
        [["TOTAL", costo_str]],
        colWidths=[120 * mm, 45 * mm],
    )
    total_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 13),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("LINEABOVE", (0, 0), (-1, 0), 1, colors.HexColor("#1a1a1a")),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    elements.append(total_table)
    elements.append(Spacer(1, 20 * mm))

    emitido = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    elements.append(
        Paragraph(
            f"Recibo generado electrónicamente el {emitido}. Documento de uso interno para "
            "reporte de gastos de viaje.",
            footer_style,
        )
    )

    doc.build(elements)
    buffer.seek(0)
    return buffer.read()


# ---------------------------------------------------------------------------
# INTERFAZ (LOGIN + FORMULARIO)
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Recibos de Viaje", page_icon="🧾", layout="centered")

if "logged_user" not in st.session_state:
    st.session_state.logged_user = None


def login_screen():
    st.title("🧾 Recibos de Viaje")
    st.caption(SERVICE_TITLE)
    with st.form("login_form"):
        username = st.text_input("Usuario").strip().lower()
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Entrar")
    if submitted:
        expected = AUTH_USERS.get(username)
        if expected and password == expected:
            st.session_state.logged_user = username
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")


def receipt_form():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🧾 Nuevo recibo de viaje")
    with col2:
        if st.button("Salir"):
            st.session_state.logged_user = None
            st.rerun()

    st.caption(f"Sesión iniciada como: **{st.session_state.logged_user}**")

    with st.form("receipt_form"):
        folio = st.text_input("Folio (escríbelo tú, ej. 0001)")
        fecha = st.date_input("Fecha del viaje", value=datetime.date.today())
        origen = st.text_input("Origen")
        destino = st.text_input("Destino")
        costo = st.number_input("Costo (MXN)", min_value=0.0, step=1.0, format="%.2f")
        forma_pago = st.selectbox("Forma de pago", ["Efectivo", "Transferencia"])
        submitted = st.form_submit_button("Generar recibo PDF")

    if submitted:
        if not folio or not origen or not destino or costo <= 0:
            st.error("Completa folio, origen, destino y un costo mayor a cero.")
            return

        pdf_bytes = build_pdf(folio, fecha, origen, destino, costo, forma_pago)
        filename = f"recibo_{folio}_{fecha.strftime('%Y%m%d')}.pdf"

        st.success(f"Recibo generado — Folio #{folio}")
        st.download_button(
            label="⬇️ Descargar PDF",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
        )


if st.session_state.logged_user is None:
    login_screen()
else:
    receipt_form()
