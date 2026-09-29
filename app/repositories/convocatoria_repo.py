from app.core.database import Database
from app.models.convocatoria import Convocatoria as ConvocatoriaModel
from fastapi import APIRouter, HTTPException


class ConvocatoriaRepository:

    def __init__(self):
        # Composición: el repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM convocatoria
                ORDER BY id_convocatoria ASC;
            """)

            registros = cursor.fetchall()

            conn.close()
            return registros
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def obtener_por_id(self, convocatoria_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM convocatoria
                WHERE id_convocatoria = %s;
            """, (convocatoria_id,))

            registro = cursor.fetchone()

            conn.close()
            return registro
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def crear(self, convocatoria: ConvocatoriaModel):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO convocatoria (
                    id_auxilio,
                    id_periodo,
                    nombre,
                    fecha_inicio,
                    fecha_fin,
                    cupos,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_convocatoria;
            """

            cursor.execute(query, (
                convocatoria.id_auxilio,
                convocatoria.id_periodo,
                convocatoria.nombre,
                convocatoria.fecha_inicio,
                convocatoria.fecha_fin,
                convocatoria.cupos,
                convocatoria.estado
            ))

            nuevo_id = cursor.fetchone()['id_convocatoria']

            conn.commit()
            conn.close()

            return nuevo_id
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def eliminar(self, convocatoria_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM convocatoria
                WHERE id_convocatoria = %s
                RETURNING id_convocatoria;
            """, (convocatoria_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def actualizar(
        self,
        convocatoria_id: int,
        convocatoria: ConvocatoriaModel
    ):
        try:  
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE convocatoria
                SET
                    id_auxilio = %s,
                    id_periodo = %s,
                    nombre = %s,
                    fecha_inicio = %s,
                    fecha_fin = %s,
                    cupos = %s,
                    estado = %s
                WHERE id_convocatoria = %s
                RETURNING id_convocatoria;
            """

            cursor.execute(query, (
                convocatoria.id_auxilio,
                convocatoria.id_periodo,
                convocatoria.nombre,
                convocatoria.fecha_inicio,
                convocatoria.fecha_fin,
                convocatoria.cupos,
                convocatoria.estado,
                convocatoria_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None