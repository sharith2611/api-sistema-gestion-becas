
from app.core.database import Database
from app.models.modulo_rol import ModuloRol
from fastapi import APIRouter, HTTPException


class ModuloRolRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulo_rol
                ORDER BY id_modulo_rol ASC;
            """)

            registros = cursor.fetchall()

            conn.close()

            return registros
        except Exception as e:
            print(f"Error de conexión a la BD: {e}")
            return None

    def obtener_por_id(self, modulo_rol_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulo_rol
                WHERE id_modulo_rol = %s;
            """, (modulo_rol_id,))

            registro = cursor.fetchone()

            conn.close()

            return registro
        except Exception as e:
            print(f"Error de conexión a la BD: {e}")
            return None

    def crear(self, modulo_rol: ModuloRol):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO modulo_rol
                (id_rol, id_modulo, estado)
                VALUES (%s, %s, %s)
                RETURNING id_modulo_rol;
            """

            cursor.execute(
                query,
                (
                    modulo_rol.id_rol,
                    modulo_rol.id_modulo,
                    modulo_rol.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_modulo_rol"]

            conn.commit()
            conn.close()

            return nuevo_id
        except Exception as e:
            print(f"Error de conexión a la BD: {e}")
            return None

    def eliminar(self, modulo_rol_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM modulo_rol
                WHERE id_modulo_rol = %s
                RETURNING id_modulo_rol;
            """, (modulo_rol_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None
        except Exception as e:
            print(f"Error de conexión a la BD: {e}")
            return None

    def actualizar(self, modulo_rol_id: int, modulo_rol: ModuloRol):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE modulo_rol
                SET id_rol = %s,
                    id_modulo = %s,
                    estado = %s,
                    actualizado = CURRENT_TIMESTAMP
                WHERE id_modulo_rol = %s
                RETURNING id_modulo_rol;
            """

            cursor.execute(
                query,
                (
                    modulo_rol.id_rol,
                    modulo_rol.id_modulo,
                    modulo_rol.estado,
                    modulo_rol_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None
        except Exception as e:
            print(f"Error de conexión a la BD: {e}")
            return None
        
        
    def obtener_por_rol(self, id_rol: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    mr.id_modulo_rol,
                    mr.id_rol,
                    mr.id_modulo,
                    m.nombre AS nombre_modulo,
                    mr.estado,
                    mr.creado,
                    mr.actualizado
                FROM modulo_rol mr
                INNER JOIN modulo m
                    ON m.id_modulo = mr.id_modulo
                WHERE mr.id_rol = %s
                  AND mr.estado = TRUE
                  AND m.estado = TRUE
                ORDER BY mr.id_modulo ASC;
            """, (id_rol,))

            registros = cursor.fetchall()

            conn.close()

            return registros

        except Exception as e:
            print(f"Error al obtener módulos del rol: {e}")
            return None

