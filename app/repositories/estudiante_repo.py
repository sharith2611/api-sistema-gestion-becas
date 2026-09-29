from app.core.database import Database
from app.models.estudiante import Estudiante
from fastapi import APIRouter, HTTPException



class EstudianteRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM estudiante ORDER BY id_estudiante ASC;"
            )

            registros = cursor.fetchall()

            conn.close()

            return registros
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def obtener_por_id(self, id_estudiante: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM estudiante WHERE id_estudiante=%s;",
                (id_estudiante,)
            )

            registro = cursor.fetchone()

            conn.close()

            return registro
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def obtener_por_programa(self, id_programa: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM estudiante WHERE id_programa=%s;",
                (id_programa,)
            )

            registros = cursor.fetchall()

            conn.close()

            return registros
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def crear(self, estudiante: Estudiante):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO estudiante
            (id_programa,documento,nombres,apellidos,email,telefono,fecha_ingreso,estado)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING id_estudiante;
            """

            cursor.execute(query, (
                estudiante.id_programa,
                estudiante.documento,
                estudiante.nombres,
                estudiante.apellidos,
                estudiante.email,
                estudiante.telefono,
                estudiante.fecha_ingreso,
                estudiante.estado
            ))

            nuevo_id = cursor.fetchone()["id_estudiante"]

            conn.commit()
            conn.close()

            return nuevo_id
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None