from app.core.database import Database
from app.models.usuario import Usuario
from fastapi import APIRouter, HTTPException


class UsuarioRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM usuario
                ORDER BY id_usuario ASC;
            """)

            usuarios = cursor.fetchall()

            conn.close()

            return usuarios
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def obtener_por_id(self, usuario_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM usuario
                WHERE id_usuario = %s;
            """, (usuario_id,))

            usuario = cursor.fetchone()

            conn.close()

            return usuario
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def crear(self, usuario: Usuario):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO usuario
                (id_usuario, nombre, cedula, telefono, nivel,estado)
                VALUES (%s, %s, %s, %s, %s,%s)
                RETURNING id_usuario;
            """

            cursor.execute(
                query,
                (
                    usuario.id_usuario,
                    usuario.nombre,
                    usuario.cedula,
                    usuario.telefono,
                    usuario.nivel,
                    usuario.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_usuario"]

            conn.commit()
            conn.close()

            return nuevo_id
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def eliminar(self, usuario_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM usuario
                WHERE id_usuario = %s
                RETURNING id_usuario;
            """, (usuario_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None
        except Exception as e:
                   print(f"Error de conexión a la BD: {e}")
                   return None

    def actualizar(self, usuario_id: int, usuario: Usuario):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE usuario
                SET nombre = %s,
                    cedula = %s,
                    telefono = %s,
                    nivel = %s,
                    estado= %s
                WHERE id_usuario = %s
                RETURNING id_usuario;
            """

            cursor.execute(
                query,
                (
                    usuario.nombre,
                    usuario.cedula,
                    usuario.telefono,
                    usuario.nivel,
                    usuario_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None