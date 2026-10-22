import logging

from fastapi import APIRouter, HTTPException

from app.repositories.repositorio_auth import RepositorioAuth
from app.models.LoginRequest import LoginRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Autenticación"])

repositorio_auth = RepositorioAuth()


@router.post("/login")
def iniciar_sesion(datos: LoginRequest):
    """
    Recibe las credenciales y delega la autenticación
    al repositorio.
    """
    try:
        resultado = repositorio_auth.iniciar_sesion(
            codigo_usuario=datos.codigo_usuario,
            clave=datos.clave
        )

        return resultado

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible conectar con la base de datos."
        )

    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )

    except Exception:
        logger.exception("Error durante el inicio de sesión")
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al intentar iniciar sesión."
        )