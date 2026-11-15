"""Endpoints de historial de postulaciones para el estudiante autenticado.

Requiere que el login de tu sistema emita un JWT HS256 con:
- sub: documento del usuario
- exp: fecha de expiración
Y que el cliente envíe Authorization: Bearer <token>.

Si tu login usa cookies o una autenticación diferente, adapta
obtener_documento_autenticado a ese mecanismo real.
"""
import io
import os

import jwt
from jwt import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.repositories.historial_repo import HistorialPersonalRepository
from app.api.rutas_reporte import crear_pdf, crear_excel

router = APIRouter(prefix='/postulaciones/mi-historial', tags=['Mi historial de postulaciones'])
repo = HistorialPersonalRepository()
seguridad = HTTPBearer(auto_error=False)


def obtener_documento_autenticado(
    credenciales: HTTPAuthorizationCredentials | None = Depends(seguridad),
) -> str:
    if credenciales is None or credenciales.scheme.lower() != 'bearer':
        raise HTTPException(status_code=401, detail='Debes iniciar sesión para descargar el historial.')

    secreto = os.getenv('JWT_SECRET')
    if not secreto:
        raise HTTPException(status_code=503, detail='Falta configurar JWT_SECRET en el backend.')

    try:
        datos = jwt.decode(
            credenciales.credentials,
            secreto,
            algorithms=['HS256'],
            options={'require': ['sub', 'exp']},
        )
    except InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail='Sesión inválida o vencida.') from exc

    documento = datos.get('sub')
    if not isinstance(documento, str) or not documento.strip():
        raise HTTPException(status_code=401, detail='La sesión no identifica al estudiante.')

    return documento.strip()


def registros_estudiante(documento: str):
    registros = repo.consultar_por_documento(documento)
    if not registros:
        raise HTTPException(status_code=404, detail='No tienes postulaciones registradas.')
    return registros


@router.get('/pdf/')
def historial_pdf(documento: str = Depends(obtener_documento_autenticado)):
    registros = registros_estudiante(documento)
    archivo = crear_pdf(registros, tipo='postulaciones')
    return StreamingResponse(
        io.BytesIO(archivo),
        media_type='application/pdf',
        headers={'Content-Disposition': 'attachment; filename="mi_historial_postulaciones.pdf"'},
    )


@router.get('/excel/')
def historial_excel(documento: str = Depends(obtener_documento_autenticado)):
    registros = registros_estudiante(documento)
    archivo = crear_excel(registros, tipo='postulaciones')
    return StreamingResponse(
        io.BytesIO(archivo),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename="mi_historial_postulaciones.xlsx"'},
    )
