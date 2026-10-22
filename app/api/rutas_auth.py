
import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from app.core.database import Database


router = APIRouter(prefix="/auth", tags=["Autenticación"])

db = Database()
password_hash = PasswordHash.recommended()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
TOKEN_DURATION_MINUTES = 60


class LoginRequest(BaseModel):
    codigo_usuario: str
    clave: str


def verificar_y_actualizar_clave(clave_ingresada: str, clave_guardada: str, id_usuario: int, conn) -> bool:
    """
    Acepta contraseñas antiguas en texto normal.
    Si son correctas, las convierte a hash y actualiza la BD.
    Las contraseñas que ya están en formato Argon2 se verifican directamente.
    """

    if not clave_guardada:
        return False

    if clave_guardada.startswith("$argon2"):
        try:
            return password_hash.verify(clave_ingresada, clave_guardada)
        except Exception:
            return False

    # Compatibilidad temporal con las contraseñas antiguas en texto normal.
    if clave_ingresada != clave_guardada:
        return False

    nueva_clave_hash = password_hash.hash(clave_ingresada)

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE usuario
            SET clave = %s
            WHERE id_usuario = %s
            """,
            (nueva_clave_hash, id_usuario)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()

    return True


@router.post("/login")
def iniciar_sesion(datos: LoginRequest):
    if not JWT_SECRET_KEY:
        raise HTTPException(
            status_code=500,
            detail="La autenticación no está configurada en el servidor."
        )

    conn = db.get_connection()

    if conn is None:
        raise HTTPException(
            status_code=503,
            detail="No fue posible conectar con la base de datos."
        )

    try:
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    id_usuario,
                    codigo_usuario,
                    nombre,
                    cedula,
                    id_rol,
                    estado,
                    clave
                FROM usuario
                WHERE codigo_usuario = %s
                LIMIT 1
                """,
                (datos.codigo_usuario.strip(),)
            )

            usuario = cursor.fetchone()
        finally:
            cursor.close()

        if not usuario:
            raise HTTPException(
                status_code=401,
                detail="Código de usuario o contraseña incorrectos."
            )

        if not usuario["estado"]:
            raise HTTPException(
                status_code=403,
                detail="El usuario está inactivo."
            )

        clave_correcta = verificar_y_actualizar_clave(
            clave_ingresada=datos.clave,
            clave_guardada=usuario["clave"],
            id_usuario=usuario["id_usuario"],
            conn=conn
        )

        if not clave_correcta:
            raise HTTPException(
                status_code=401,
                detail="Código de usuario o contraseña incorrectos."
            )

        ahora = datetime.now(timezone.utc)

        payload = {
            "sub": str(usuario["id_usuario"]),
            "id_usuario": usuario["id_usuario"],
            "codigo_usuario": usuario["codigo_usuario"],
            "nombre": usuario["nombre"],
            "id_rol": usuario["id_rol"],
            "iat": ahora,
            "exp": ahora + timedelta(minutes=TOKEN_DURATION_MINUTES)
        }

        token = jwt.encode(
            payload,
            JWT_SECRET_KEY,
            algorithm=JWT_ALGORITHM
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": {
                "id_usuario": usuario["id_usuario"],
                "codigo_usuario": usuario["codigo_usuario"],
                "nombre": usuario["nombre"],
                "cedula": usuario["cedula"],
                "id_rol": usuario["id_rol"]
            }
        }

    finally:
        conn.close()
