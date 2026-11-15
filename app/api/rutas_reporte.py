import base64
import io
import json
import os
import urllib.error
import urllib.request
from datetime import date, datetime
from html import escape
from typing import Literal

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, LongTable, TableStyle, Paragraph, Spacer

from app.repositories.reporte_repo import ReporteRepository

router = APIRouter(prefix='/reportes', tags=['Reportes'])
repo = ReporteRepository()


COLUMNAS_POSTULACIONES = [
    ('estudiante', 'Estudiante'), ('institucion', 'Institución'),
    ('facultad', 'Facultad'), ('programa', 'Programa'),
    ('convocatoria', 'Convocatoria'), ('auxilio', 'Auxilio educativo'),
    ('fecha', 'Fecha'), ('escala', 'Escala'),
]
COLUMNAS_ESTUDIANTES = [
    ('estudiante', 'Estudiante'), ('correo', 'Correo electrónico'),
    ('telefono', 'Teléfono'), ('institucion', 'Institución'),
    ('facultad', 'Facultad'), ('programa', 'Programa'),
    ('fecha', 'Fecha ingreso'), ('estado_estudiante', 'Estado'),
]
TIPO_REPORTE = Literal['postulaciones', 'estudiantes']


def metadatos(tipo):
    if tipo == 'estudiantes':
        return COLUMNAS_ESTUDIANTES, 'Reporte de estudiantes registrados', 'reporte_estudiantes'
    return COLUMNAS_POSTULACIONES, 'Reporte de postulaciones', 'reporte_postulaciones'


def validar_fechas(inicio, fin):
    if inicio and fin and fin < inicio:
        raise HTTPException(422, 'La fecha final no puede ser menor que la inicial.')



def obtener_registros(fecha_inicio=None, fecha_fin=None, escala=None,
                      id_convocatoria=None, tipo='postulaciones',
                      id_programa=None, estado_estudiante=None):
    validar_fechas(fecha_inicio, fecha_fin)
    if tipo == 'estudiantes':
        return repo.consultar_estudiantes(fecha_inicio, fecha_fin,
                                         id_programa, estado_estudiante)
    return repo.consultar(fecha_inicio, fecha_fin, escala, id_convocatoria)


def crear_pdf(registros, tipo="postulaciones"):
    columnas, nombre_reporte, _ = metadatos(tipo)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=landscape(A4),
        rightMargin=25, leftMargin=25, topMargin=40, bottomMargin=40
    )
    estilos = getSampleStyleSheet()
    titulo = ParagraphStyle(
        'TituloReporte', parent=estilos['Title'],
        textColor=colors.HexColor('#174A91'), fontSize=17, spaceAfter=8
    )
    celda = ParagraphStyle('CeldaReporte', parent=estilos['Normal'], fontSize=7, leading=9)
    encabezado = ParagraphStyle(
        'EncabezadoReporte', parent=celda,
        textColor=colors.white, fontName='Helvetica-Bold'
    )
    contenido = [
        Paragraph('Sistema de Becas y Ayudas Económicas', titulo),
        Paragraph(nombre_reporte, estilos['Heading2']),
        Paragraph(
            f'Generado: {datetime.now():%d/%m/%Y %H:%M} | Registros: {len(registros)}',
            estilos['Normal']
        ),
        Spacer(1, 12),
    ]
    filas = [[Paragraph(escape(t), encabezado) for _, t in columnas]]
    for registro in registros:
        filas.append([
            Paragraph(escape(str(registro.get(clave) or '')), celda)
            for clave, _ in columnas
        ])
    anchos = [100, 83, 75, 88, 100, 94, 65, 70] if tipo == "postulaciones" else [97, 110, 70, 100, 94, 93, 70, 53]
    tabla = LongTable(filas, colWidths=anchos, repeatRows=1, hAlign='LEFT')
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#174A91')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#EFF4FA')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#174A91')),
    ]))
    contenido.append(tabla)

    def pie(canvas, documento):
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor('#617084'))
        canvas.drawString(25, 22, 'Sistema de Gestión de Becas y Ayudas Económicas')
        canvas.drawRightString(landscape(A4)[0] - 25, 22, f'Página {documento.page}')

    doc.build(contenido, onFirstPage=pie, onLaterPages=pie)
    return buffer.getvalue()


def crear_excel(registros, tipo="postulaciones"):
    columnas, nombre_reporte, _ = metadatos(tipo)
    wb = Workbook()
    ws = wb.active
    ws.title = 'Estudiantes' if tipo == 'estudiantes' else 'Postulaciones'
    cantidad_columnas = len(columnas)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=cantidad_columnas)
    ws.cell(1, 1, 'SISTEMA DE BECAS Y AYUDAS ECONÓMICAS')
    ws.cell(1, 1).font = Font(bold=True, size=16, color='FFFFFF')
    ws.cell(1, 1).fill = PatternFill('solid', fgColor='174A91')
    ws.cell(2, 1, f'{nombre_reporte} | {datetime.now():%d/%m/%Y %H:%M} | Total: {len(registros)}')
    for j, (_, nombre) in enumerate(columnas, start=1):
        celda = ws.cell(4, j, nombre)
        celda.fill = PatternFill('solid', fgColor='174A91')
        celda.font = Font(bold=True, color='FFFFFF')
        celda.alignment = Alignment(wrap_text=True)
    for i, registro in enumerate(registros, start=5):
        for j, (clave, _) in enumerate(columnas, start=1):
            valor = registro.get(clave)
            # Evita que valores de texto ingresados en la base ejecuten fórmulas de Excel.
            if isinstance(valor, str) and valor.lstrip().startswith(('=', '+', '-', '@')):
                valor = "'" + valor
            celda = ws.cell(i, j, valor if valor is not None else '')
            celda.alignment = Alignment(vertical='top', wrap_text=True)
            if i % 2 == 0:
                celda.fill = PatternFill('solid', fgColor='EFF4FA')
        # Anchos específicos para cada modalidad.
    anchos = [30, 25, 24, 28, 29, 26, 15, 18] if tipo == 'postulaciones' else [30, 34, 20, 27, 26, 30, 18, 16]
    for j, ancho in enumerate(anchos, start=1):
        ws.column_dimensions[get_column_letter(j)].width = ancho
    ws.freeze_panes = 'A5'
    ws.auto_filter.ref = f'A4:{get_column_letter(cantidad_columnas)}{max(4, 4 + len(registros))}'
    buffer = io.BytesIO()
    wb.save(buffer)
    return buffer.getvalue()



@router.get('/opciones/')
def opciones():
    return {
        'convocatorias': repo.obtener_convocatorias(),
        'escalas': repo.obtener_escalas(),
        'programas': repo.obtener_programas(),
    }


@router.get('/vista-previa/')
def vista_previa(tipo: TIPO_REPORTE = 'postulaciones', fecha_inicio: date | None = None,
                 fecha_fin: date | None = None, escala: str | None = None,
                 id_convocatoria: int | None = None, id_programa: int | None = None,
                 estado_estudiante: bool | None = None):
    return obtener_registros(fecha_inicio, fecha_fin, escala, id_convocatoria,
                            tipo, id_programa, estado_estudiante)


@router.get('/pdf/')
def descargar_pdf(tipo: TIPO_REPORTE = 'postulaciones', fecha_inicio: date | None = None,
                  fecha_fin: date | None = None, escala: str | None = None,
                  id_convocatoria: int | None = None, id_programa: int | None = None,
                  estado_estudiante: bool | None = None):
    registros = obtener_registros(fecha_inicio, fecha_fin, escala, id_convocatoria,
                                 tipo, id_programa, estado_estudiante)
    data = crear_pdf(registros, tipo)
    _, _, nombre = metadatos(tipo)
    return StreamingResponse(io.BytesIO(data), media_type='application/pdf',
        headers={'Content-Disposition': f'attachment; filename="{nombre}.pdf"'})


@router.get('/excel/')
def descargar_excel(tipo: TIPO_REPORTE = 'postulaciones', fecha_inicio: date | None = None,
                    fecha_fin: date | None = None, escala: str | None = None,
                    id_convocatoria: int | None = None, id_programa: int | None = None,
                    estado_estudiante: bool | None = None):
    registros = obtener_registros(fecha_inicio, fecha_fin, escala, id_convocatoria,
                                 tipo, id_programa, estado_estudiante)
    data = crear_excel(registros, tipo)
    _, _, nombre = metadatos(tipo)
    return StreamingResponse(io.BytesIO(data),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename="{nombre}.xlsx"'})


class EnvioCorreo(BaseModel):
    destinatario: EmailStr
    formato: Literal['pdf', 'excel'] = 'pdf'
    tipo: TIPO_REPORTE = 'postulaciones'
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    escala: str | None = None
    id_convocatoria: int | None = None
    id_programa: int | None = None
    estado_estudiante: bool | None = None


@router.post('/enviar-correo/')
def enviar_correo(solicitud: EnvioCorreo):
    """Genera un PDF o Excel y solicita su envío a Resend mediante HTTPS."""
    api_key = os.getenv('RESEND_API_KEY')
    remitente = os.getenv('RESEND_FROM', 'Sistema de Becas <onboarding@resend.dev>')

    if not api_key:
        raise HTTPException(503, 'No se ha configurado RESEND_API_KEY.')

    registros = obtener_registros(
        solicitud.fecha_inicio,
        solicitud.fecha_fin,
        solicitud.escala,
        solicitud.id_convocatoria,
        solicitud.tipo,
        solicitud.id_programa,
        solicitud.estado_estudiante,
    )

    _, _, prefijo = metadatos(solicitud.tipo)
    if solicitud.formato == 'pdf':
        archivo = crear_pdf(registros, solicitud.tipo)
        nombre = f'{prefijo}.pdf'
    else:
        archivo = crear_excel(registros, solicitud.tipo)
        nombre = f'{prefijo}.xlsx'

    contenido_base64 = base64.b64encode(archivo).decode('ascii')
    payload = {
        'from': remitente,
        'to': [str(solicitud.destinatario)],
        'subject': 'Reporte de estudiantes registrados' if solicitud.tipo == 'estudiantes' else 'Reporte de postulaciones',
        'text': 'Adjuntamos el reporte solicitado desde el Sistema de Becas y Ayudas Económicas.',
        'attachments': [{'filename': nombre, 'content': contenido_base64}],
    }

    peticion = urllib.request.Request(
        'https://api.resend.com/emails',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            # Evita la identificación predeterminada "Python-urllib/...".
            # Es una prueba para el bloqueo Cloudflare 1010, no una garantía.
            'User-Agent': 'SistemaGestionBecas/1.0 (Python; Resend HTTPS Client)',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(peticion, timeout=20) as respuesta:
            resultado = json.load(respuesta)
    except urllib.error.HTTPError as exc:
        detalle = exc.read(1000).decode('utf-8', errors='replace')
        print(f'Error de Resend HTTP {exc.code}: {detalle}')

        # Cloudflare 1010 es un bloqueo del cliente HTTP antes de que la API
        # pueda evaluar normalmente remitente, destinatario o credenciales.
        if exc.code == 403 and 'error code: 1010' in detalle.lower():
            raise HTTPException(
                502,
                'La protección de red bloqueó la solicitud a Resend (Cloudflare 1010). '
                'Revisa los logs; puede requerir usar el SDK oficial o contactar al proveedor.'
            ) from exc

        if exc.code == 401:
            raise HTTPException(502, 'Resend rechazó la clave API. Verifica RESEND_API_KEY.') from exc
        if exc.code in (400, 403, 422):
            raise HTTPException(
                502,
                'Resend rechazó el envío. Revisa los logs para conocer el motivo exacto.'
            ) from exc
        raise HTTPException(502, 'Error del proveedor de correo al enviar el reporte.') from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f'Error de conexión con Resend: {type(exc).__name__}: {exc}')
        raise HTTPException(502, 'No fue posible conectar con el servicio de correo.') from exc

    return {
        'mensaje': 'Reporte aceptado por el servicio de correo.',
        'id_envio': resultado.get('id'),
    }
