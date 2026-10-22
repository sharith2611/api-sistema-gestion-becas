import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.database import Database


class RepositorioAuth:
    def __init__(self):
        self.db = Database()
        self.password_hash = PasswordHash.recommended()

    def obtener_usuario_por_codigo(self, codigo_usuario: str):
        """
        Consulta un usuario por su código.
        """
        conn = self.db.get_connection()

        if conn is None:
            raise ConnectionError(
                "No fue posible conectar con la base de datos."
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
                    WHERE LOWER(TRIM(codigo_usuario)) = LOWER(%s)
                    LIMIT 1
                    """,
                    (codigo_usuario.strip(),)
                )

                return cursor.fetchone()

            finally:
                cursor.close()

        finally:
            conn.close()

    def verificar_y_actualizar_clave(
        self,
        clave_ingresada: str,
        clave_guardada: str,
        id_usuario: int
    ) -> bool:
        """
        Verifica la contraseña del usuario.

        Las contraseñas Argon2 se verifican mediante PasswordHash.
        Las contraseñas antiguas en texto plano se aceptan temporalmente
        y, si coinciden, se convierten a hash Argon2.
        """
        if not clave_guardada:
            return False

        # Si la contraseña ya está almacenada como hash Argon2.
        if clave_guardada.startswith("$argon2"):
            try:
                return self.password_hash.verify(
                    clave_ingresada,
                    clave_guardada
                )
            except Exception:
                return False

        # Compatibilidad temporal con contraseñas antiguas en texto plano.
        if clave_ingresada != clave_guardada:
            return False

        # Convertir la contraseña correcta a hash Argon2.
        nueva_clave_hash = self.password_hash.hash(clave_ingresada)

        conn = self.db.get_connection()

        if conn is None:
            raise ConnectionError(
                "No fue posible conectar con la base de datos."
            )

        try:
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

        finally:
            conn.close()

        return True

    def iniciar_sesion(self, codigo_usuario: str, clave: str):
        """
        Valida las credenciales y genera un token JWT.
        """
        usuario = self.obtener_usuario_por_codigo(codigo_usuario)

        if not usuario:
            raise ValueError(
                "Código de usuario o contraseña incorrectos."
            )

        if not usuario["estado"]:
            raise PermissionError("El usuario está inactivo.")

        clave_correcta = self.verificar_y_actualizar_clave(
            clave_ingresada=clave,
            clave_guardada=usuario["clave"],
            id_usuario=usuario["id_usuario"]
        )

        if not clave_correcta:
            raise ValueError(
                "Código de usuario o contraseña incorrectos."
            )

        # Esta clave es independiente de la contraseña del usuario.
        jwt_secret_key = os.getenv("JWT_SECRET_KEY")

        if not jwt_secret_key:
            raise RuntimeError(
                "Falta configurar JWT_SECRET_KEY en las variables "
                "de entorno del backend."
            )

        ahora = datetime.now(timezone.utc)

        payload = {
            "sub": str(usuario["id_usuario"]),
            "id_usuario": usuario["id_usuario"],
            "codigo_usuario": usuario["codigo_usuario"],
            "nombre": usuario["nombre"],
            "id_rol": usuario["id_rol"],
            "iat": ahora,
            "exp": ahora + timedelta(minutes=60)
        }

        token = jwt.encode(
            payload,
            jwt_secret_key,
            algorithm="HS256"
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