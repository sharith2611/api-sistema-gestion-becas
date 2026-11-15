
"""
Historial personal de postulaciones.

Utiliza el JWT generado por POST /auth/login.
El token contiene sub = id_usuario.

Permite descargar únicamente las postulaciones
asociadas al usuario autenticado.
"""

import io
import os

import jwt

from jwt import InvalidTokenError

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.responses import StreamingResponse

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)

from app.repositories.historial_repo import HistorialPersonalRepository

from app.api.rutas_reporte import (
    crear_pdf,
    crear_excel
)


# ============================================================
# CONFIGURACIÓN DEL ROUTER
# ============================================================

router = APIRouter(
    prefix="/postulaciones/mi-historial",
    tags=["Mi historial de postulaciones"]
)

repo = HistorialPersonalRepository()

seguridad = HTTPBearer(auto_error=False)


# ============================================================
# 1. VALIDAR EL TOKEN JWT
# ============================================================

def obtener_usuario_autenticado(
    credenciales: HTTPAuthorizationCredentials | None = Depends(seguridad)
) -> int:

    # Comprobar que el frontend envió el token
    if (
        credenciales is None
        or credenciales.scheme.lower() != "bearer"
    ):
        raise HTTPException(
            status_code=401,
            detail="Debes iniciar sesión para descargar el historial."
        )

    # Misma clave utilizada por RepositorioAuth
    jwt_secret_key = os.getenv("JWT_SECRET_KEY")

    if not jwt_secret_key:
        raise HTTPException(
            status_code=503,
            detail="No está configurada JWT_SECRET_KEY en el backend."
        )

    try:
        # Validar la firma y vencimiento del JWT
        datos = jwt.decode(
            credenciales.credentials,
            jwt_secret_key,
            algorithms=["HS256"],
            options={
                "require": ["sub", "exp"]
            }
        )

    except InvalidTokenError as error:
        raise HTTPException(
            status_code=401,
            detail="Tu sesión es inválida o ha expirado."
        ) from error

    # El login guarda el id_usuario dentro de sub
    try:
        id_usuario = int(datos["sub"])

        if id_usuario <= 0:
            raise ValueError("Identificador inválido")

    except (ValueError, TypeError, KeyError) as error:
        raise HTTPException(
            status_code=401,
            detail="El token no contiene un usuario válido."
        ) from error

    return id_usuario


# ============================================================
# 2. CONSULTAR POSTULACIONES DEL USUARIO
# ============================================================

def obtener_postulaciones_personales(id_usuario: int):

    registros = repo.consultar_por_usuario_id(id_usuario)

    if not registros:
        raise HTTPException(
            status_code=404,
            detail="No tienes postulaciones registradas."
        )

    return registros


# ============================================================
# 3. DESCARGAR HISTORIAL EN PDF
# ============================================================

@router.get("/pdf/")
def historial_pdf(
    id_usuario: int = Depends(obtener_usuario_autenticado)
):

    registros = obtener_postulaciones_personales(id_usuario)

    archivo = crear_pdf(
        registros,
        tipo="postulaciones"
    )

    return StreamingResponse(
        io.BytesIO(archivo),
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                'attachment; filename="mi_historial_postulaciones.pdf"'
        }
    )


# ============================================================
# 4. DESCARGAR HISTORIAL EN EXCEL
# ============================================================

@router.get("/excel/")
def historial_excel(
    id_usuario: int = Depends(obtener_usuario_autenticado)
):

    registros = obtener_postulaciones_personales(id_usuario)

    archivo = crear_excel(
        registros,
        tipo="postulaciones"
    )

    return StreamingResponse(
        io.BytesIO(archivo),
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition":
                'attachment; filename="mi_historial_postulaciones.xlsx"'
        }
    )
