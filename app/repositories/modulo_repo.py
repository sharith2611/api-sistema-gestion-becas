from app.core.database import Database
from app.models.modulo import Modulo
from fastapi import APIRouter, HTTPException



class ModuloRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulo
                ORDER BY id_modulo ASC;
            """)

            modulos = cursor.fetchall()

            conn.close()

            return modulos
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None


    def obtener_por_id(self, modulo_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulo
                WHERE id_modulo = %s;
            """, (modulo_id,))

            modulo = cursor.fetchone()

            conn.close()

            return modulo
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def crear(self, modulo: Modulo):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO modulo
                (id_modulo, nombre,estado)
                VALUES (%s,%s, %s)
                RETURNING id_modulo;
            """

            cursor.execute(
                query,
                (
                    modulo.id_modulo,
                    modulo.nombre,
                    modulo.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_modulo"]

            conn.commit()
            conn.close()

            return nuevo_id
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def eliminar(self, modulo_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM modulo
                WHERE id_modulo = %s
                RETURNING id_modulo;
            """, (modulo_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def actualizar(self, modulo_id: int, modulo: Modulo):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE modulo
                SET nombre = %s,
                    estado=%s
                WHERE id_modulo = %s
                RETURNING id_modulo;
            """

            cursor.execute(
                query,
                (
                    modulo.nombre,
                    modulo.estado,
                    modulo_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None