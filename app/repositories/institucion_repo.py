from app.core.database import Database
from app.models.institucion import Institucion
from fastapi import APIRouter, HTTPException



class InstitucionRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM institucion ORDER BY id_institucion ASC;")

            registros = cursor.fetchall()

            conn.close()

            return registros
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def obtener_por_id(self, id_institucion: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM institucion WHERE id_institucion = %s;",
                (id_institucion,)
            )

            registro = cursor.fetchone()

            conn.close()

            return registro
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def crear(self, institucion: Institucion):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO institucion
            (nombre,direccion,telefono,email,estado)
            VALUES (%s,%s,%s,%s,%s)
            RETURNING id_institucion;
            """

            cursor.execute(query, (
                institucion.nombre,
                institucion.direccion,
                institucion.telefono,
                institucion.email,
                institucion.estado
            ))

            nuevo_id = cursor.fetchone()["id_institucion"]

            conn.commit()
            conn.close()

            return nuevo_id
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def actualizar(self, id_institucion: int, institucion: Institucion):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
            UPDATE institucion
            SET nombre=%s,direccion=%s,telefono=%s,email=%s,estado=%s
            WHERE id_institucion=%s
            RETURNING id_institucion;
            """

            cursor.execute(query, (
                institucion.nombre,
                institucion.direccion,
                institucion.telefono,
                institucion.email,
                institucion.estado,
                id_institucion
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def eliminar(self,id_institucion: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM institucion WHERE id = %s RETURNING id_institucion;", (id_institucion,))
            eliminado = cursor.fetchone()
            conn.commit()
            conn.close()
            return eliminado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None