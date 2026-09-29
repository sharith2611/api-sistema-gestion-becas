from app.core.database import Database
from app.models.requisito_convocatoria import RequisitoConvocatoria
from fastapi import APIRouter, HTTPException
import logging

logger = logging.getLogger(__name__)



class RequisitoConvocatoriaRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM requisito_convocatoria ORDER BY id_requisito_convocatoria ASC;"
            )

            registros = cursor.fetchall()
            conn.close()

            return registros
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None


    def obtener_por_id(self, id_requisito_convocatoria: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM requisito_convocatoria
                WHERE id_requisito_convocatoria = %s;
                """,
                (id_requisito_convocatoria,)
            )

            registro = cursor.fetchone()

            conn.close()

            return registro
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def obtener_por_convocatoria(self, id_convocatoria: int):
        try:    
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM requisito_convocatoria
                WHERE id_convocatoria = %s
                ORDER BY id_requisito_convocatoria ASC;
                """,
                (id_convocatoria,)
            )

            registros = cursor.fetchall()

            conn.close()

            return registros
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def crear(self, requisito: RequisitoConvocatoria):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO requisito_convocatoria
                (id_convocatoria, descripcion, obligatorio, valor_minimo,estado)
                VALUES (%s, %s, %s, %s,%s)
                RETURNING id_requisito_convocatoria;
            """

            cursor.execute(query, (
                requisito.id_convocatoria,
                requisito.descripcion,
                requisito.obligatorio,
                requisito.valor_minimo,
                requisito.estado
            ))

            nuevo_id = cursor.fetchone()["id_requisito_convocatoria"]

            conn.commit()
            conn.close()

            return nuevo_id
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def actualizar(
        self,
        id_requisito_convocatoria: int,
        requisito: RequisitoConvocatoria
    ):
        try:    
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE requisito_convocatoria
                SET id_convocatoria = %s,
                    descripcion = %s,
                    obligatorio = %s,
                    valor_minimo = %s,
                    estado= %s
                WHERE id_requisito_convocatoria = %s
                RETURNING id_requisito_convocatoria;
            """

            cursor.execute(query, (
                requisito.id_convocatoria,
                requisito.descripcion,
                requisito.obligatorio,
                requisito.valor_minimo,
                requisito.estado,
                id_requisito_convocatoria
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def eliminar(self, id_requisito_convocatoria: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM requisito_convocatoria
                WHERE id_requisito_convocatoria = %s
                RETURNING id_requisito_convocatoria;
                """,
                (id_requisito_convocatoria,)
            )

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None