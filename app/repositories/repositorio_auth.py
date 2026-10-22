
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
                    WHERE codigo_usuario = %s
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

        Si la contraseña está almacenada en texto normal y es correcta,
        la convierte a hash Argon2 y actualiza la base de datos.
        Si ya está cifrada mediante hash Argon2, la verifica directamente.
        """
        if not clave_guardada:
            return False

        # Verificar contraseñas almacenadas con Argon2.
        if clave_guardada.startswith("$argon2"):
            try:
                return self.password_hash.verify(
                    clave_ingresada,
                    clave_guardada
                )
            except Exception:
                return False

        # Compatibilidad temporal con contraseñas antiguas en texto normal.
        if clave_ingresada != clave_guardada:
            return False

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

            return True

        finally:
            conn.close()
