import io
import os
import smtplib
from datetime import date, datetime
from email.message import EmailMessage
from html import escape
from typing import Literal

from fastapi import APIRouter, HTTPException, Query
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

COLUMNAS = [
    ('estudiante', 'Estudiante'), ('institucion', 'Institución'),
    ('facultad', 'Facultad'), ('programa', 'Programa'),
    ('convocatoria', 'Convocatoria'), ('auxilio', 'Auxilio educativo'),
    ('fecha', 'Fecha'), ('estado', 'Estado'), ('escala', 'Escala'),
]


def validar_fechas(inicio, fin):
    if inicio and fin and fin < inicio:
        raise HTTPException(422, 'La fecha final no puede ser menor que la inicial.')


def obtener_registros(fecha_inicio=None, fecha_fin=None, escala=None, id_convocatoria=None):
    validar_fechas(fecha_inicio, fecha_fin)
    return repo.consultar(fecha_inicio, fecha_fin, escala, id_convocatoria)


def crear_pdf(registros):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                            rightMargin=25, leftMargin=25, topMargin=40, bottomMargin=40)
    estilos = getSampleStyleSheet()
    titulo = ParagraphStyle('TituloReporte', parent=estilos['Title'],
                            textColor=colors.HexColor('#174A91'), fontSize=17, spaceAfter=8)
    celda = ParagraphStyle('CeldaReporte', parent=estilos['Normal'], fontSize=7, leading=9)
    encabezado = ParagraphStyle('EncabezadoReporte', parent=celda,
                                textColor=colors.white, fontName='Helvetica-Bold')
    contenido = [Paragraph('Sistema de Becas y Ayudas Económicas', titulo),
                 Paragraph('Reporte de postulaciones', estilos['Heading2']),
                 Paragraph(f'Generado: {datetime.now():%d/%m/%Y %H:%M} | Registros: {len(registros)}', estilos['Normal']),
                 Spacer(1, 12)]
    filas = [[Paragraph(escape(t), encabezado) for _, t in COLUMNAS]]
    for registro in registros:
        filas.append([Paragraph(escape(str(registro.get(clave) or '')), celda)
                      for clave, _ in COLUMNAS])
    anchos = [96, 84, 80, 91, 100, 90, 49, 49, 49]
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


def crear_excel(registros):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Postulaciones'
    cantidad_columnas = len(COLUMNAS)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=cantidad_columnas)
    ws.cell(1, 1, 'SISTEMA DE BECAS Y AYUDAS ECONÓMICAS')
    ws.cell(1, 1).font = Font(bold=True, size=16, color='FFFFFF')
    ws.cell(1, 1).fill = PatternFill('solid', fgColor='174A91')
    ws.cell(2, 1, f'Reporte de postulaciones | {datetime.now():%d/%m/%Y %H:%M} | Total: {len(registros)}')
    for j, (_, nombre) in enumerate(COLUMNAS, start=1):
        celda = ws.cell(4, j, nombre)
        celda.fill = PatternFill('solid', fgColor='174A91')
        celda.font = Font(bold=True, color='FFFFFF')
        celda.alignment = Alignment(wrap_text=True)
    for i, registro in enumerate(registros, start=5):
        for j, (clave, _) in enumerate(COLUMNAS, start=1):
            celda = ws.cell(i, j, registro.get(clave) or '')
            celda.alignment = Alignment(vertical='top', wrap_text=True)
            if i % 2 == 0:
                celda.fill = PatternFill('solid', fgColor='EFF4FA')
    for j, ancho in enumerate([30, 25, 24, 28, 29, 26, 15, 18, 18], start=1):
        ws.column_dimensions[get_column_letter(j)].width = ancho
    ws.freeze_panes = 'A5'
    ws.auto_filter.ref = f'A4:I{max(4, 4 + len(registros))}'
    buffer = io.BytesIO()
    wb.save(buffer)
    return buffer.getvalue()


@router.get('/opciones/')
def opciones():
    return {'convocatorias': repo.obtener_convocatorias(), 'escalas': repo.obtener_escalas()}


@router.get('/vista-previa/')
def vista_previa(fecha_inicio: date | None = None, fecha_fin: date | None = None,
                 escala: str | None = None, id_convocatoria: int | None = None):
    return obtener_registros(fecha_inicio, fecha_fin, escala, id_convocatoria)


@router.get('/pdf/')
def descargar_pdf(fecha_inicio: date | None = None, fecha_fin: date | None = None,
                  escala: str | None = None, id_convocatoria: int | None = None):
    data = crear_pdf(obtener_registros(fecha_inicio, fecha_fin, escala, id_convocatoria))
    return StreamingResponse(io.BytesIO(data), media_type='application/pdf',
        headers={'Content-Disposition': 'attachment; filename="reporte_becas.pdf"'})


@router.get('/excel/')
def descargar_excel(fecha_inicio: date | None = None, fecha_fin: date | None = None,
                    escala: str | None = None, id_convocatoria: int | None = None):
    data = crear_excel(obtener_registros(fecha_inicio, fecha_fin, escala, id_convocatoria))
    return StreamingResponse(io.BytesIO(data),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename="reporte_becas.xlsx"'})


class EnvioCorreo(BaseModel):
    destinatario: EmailStr
    formato: Literal['pdf', 'excel'] = 'pdf'
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    escala: str | None = None
    id_convocatoria: int | None = None


@router.post('/enviar-correo/')
def enviar_correo(solicitud: EnvioCorreo):
    host, usuario, password = (os.getenv('SMTP_HOST'), os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
    remitente = os.getenv('SMTP_FROM') or usuario
    if not all([host, usuario, password, remitente]):
        raise HTTPException(503, 'No se ha configurado el servicio de correo SMTP.')
    registros = obtener_registros(solicitud.fecha_inicio, solicitud.fecha_fin,
                                 solicitud.escala, solicitud.id_convocatoria)
    if solicitud.formato == 'pdf':
        archivo, nombre, tipo, subtipo = crear_pdf(registros), 'reporte_becas.pdf', 'application', 'pdf'
    else:
        archivo, nombre, tipo, subtipo = (crear_excel(registros), 'reporte_becas.xlsx', 'application',
            'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    mensaje = EmailMessage()
    mensaje['Subject'] = 'Reporte de Becas y Ayudas Económicas'
    mensaje['From'] = remitente
    mensaje['To'] = str(solicitud.destinatario)
    mensaje.set_content('Adjuntamos el reporte solicitado desde el Sistema de Becas y Ayudas Económicas.')
    mensaje.add_attachment(archivo, maintype=tipo, subtype=subtipo, filename=nombre)
    try:
        puerto = int(os.getenv('SMTP_PORT', '587'))
        if os.getenv('SMTP_SSL', 'false').lower() == 'true':
            with smtplib.SMTP_SSL(host, puerto, timeout=20) as servidor:
                servidor.login(usuario, password)
                servidor.send_message(mensaje)
        else:
            with smtplib.SMTP(host, puerto, timeout=20) as servidor:
                servidor.starttls()
                servidor.login(usuario, password)
                servidor.send_message(mensaje)
    except (smtplib.SMTPException, OSError) as exc:
        raise HTTPException(502, 'No se pudo enviar el correo. Revisa la configuración SMTP.') from exc
    return {'mensaje': 'Reporte enviado correctamente'}
