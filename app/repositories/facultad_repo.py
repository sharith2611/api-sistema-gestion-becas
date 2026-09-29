from app.core.database import Database
from app.models.facultad import Facultad
from fastapi import APIRouter, HTTPException




class FacultadRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM facultad ORDER BY id_facultad ASC;"
            )

            registros = cursor.fetchall()
            conn.close()

            return registros
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None


    def obtener_por_id(self, id_facultad: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM facultad
                WHERE id_facultad = %s;
                """,
                (id_facultad,)
            )

            registro = cursor.fetchone()

            conn.close()

            return registro
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def obtener_por_institucion(self, id_institucion: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM facultad
                WHERE id_institucion = %s
                ORDER BY id_facultad ASC;
                """,
                (id_institucion,)
            )

            registros = cursor.fetchall()

            conn.close()

            return registros
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def crear(self, facultad: Facultad):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO facultad
                (id_institucion, nombre, direccion, ext, email, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_facultad;
            """

            cursor.execute(query, (
                facultad.id_institucion,
                facultad.nombre,
                facultad.direccion,
                facultad.Ext,
                facultad.email,
                facultad.estado
            ))

            nuevo_id = cursor.fetchone()["id_facultad"]

            conn.commit()
            conn.close()

            return nuevo_id
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None
                
                
    def actualizar(self, id_facultad: int, facultad: Facultad):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE facultad
                SET id_institucion = %s,
                    nombre = %s,
                    direccion = %s,
                    ext = %s,
                    email = %s,
                    estado = %s
                WHERE id_facultad = %s
                RETURNING id_facultad;
            """

            cursor.execute(query, (
                facultad.id_institucion,
                facultad.nombre,
                facultad.direccion,
                facultad.Ext,
                facultad.email,
                facultad.estado,
                id_facultad
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None
        except Exception as e:
                   print(f"Error de conexión a la BD: {e}")
                   return None


    def eliminar(self, id_facultad: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM facultad
                WHERE id_facultad = %s
                RETURNING id_facultad;
                """,
                (id_facultad,)
            )

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None