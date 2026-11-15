"""Historial personal: valida el JWT de /auth/login (sub=id_usuario)."""
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


def obtener_usuario_autenticado(
    credenciales: HTTPAuthorizationCredentials | None = Depends(seguridad),
) -> int:
    if credenciales is None or credenciales.scheme.lower() != 'bearer':
        raise HTTPException(401, 'Debes iniciar sesión para descargar el historial.')

    secreto = os.getenv('JWT_SECRET_KEY')
    if not secreto:
        raise HTTPException(503, 'Falta configurar JWT_SECRET_KEY en el backend.')

    try:
        datos = jwt.decode(
            credenciales.credentials,
            secreto,
            algorithms=['HS256'],
            options={'require': ['sub', 'exp']},
        )
    except InvalidTokenError as exc:
        raise HTTPException(401, 'Sesión inválida o vencida.') from exc

    try:
        id_usuario = int(datos['sub'])
        if id_usuario <= 0:
            raise ValueError()
    except (ValueError, TypeError, KeyError) as exc:
        raise HTTPException(401, 'El token no identifica un usuario válido.') from exc

    return id_usuario


def registros_estudiante(id_usuario: int):
    registros = repo.consultar_por_usuario_id(id_usuario)
    if not registros:
        raise HTTPException(404, 'No hay postulaciones asociadas a este usuario activo.')
    return registros


@router.get('/pdf/')
def historial_pdf(id_usuario: int = Depends(obtener_usuario_autenticado)):
    registros = registros_estudiante(id_usuario)
    archivo = crear_pdf(registros, tipo='postulaciones')
    return StreamingResponse(
        io.BytesIO(archivo),
        media_type='application/pdf',
        headers={'Content-Disposition': 'attachment; filename="mi_historial_postulaciones.pdf"'},
    )


@router.get('/excel/')
def historial_excel(id_usuario: int = Depends(obtener_usuario_autenticado)):
    registros = registros_estudiante(id_usuario)
    archivo = crear_excel(registros, tipo='postulaciones')
    return StreamingResponse(
        io.BytesIO(archivo),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename="mi_historial_postulaciones.xlsx"'},
    )
