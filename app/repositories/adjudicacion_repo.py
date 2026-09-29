from app.core.database import Database
from app.models.adjudicacion import Adjudicacion as AdjudicacionModel
from fastapi import APIRouter, HTTPException
import logging


logger = logging.getLogger(__name__)

class AdjudicacionRepository:

    def __init__(self):
        # Composición: el repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM adjudicacion
                ORDER BY id_adjudicacion ASC;
            """)

            registros = cursor.fetchall()

            conn.close()
            return registros
        except:
            logger.exception("Error al listar los roles")
            raise HTTPException(
            status_code=500,
            detail="Error interno al obtener los roles"
            )
        

    def obtener_por_id(self, adjudicacion_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM adjudicacion
                WHERE id_adjudicacion = %s;
            """, (adjudicacion_id,))

            registro = cursor.fetchone()

            conn.close()
            return registro
        except:
            logger.exception("Error al listar los roles")
            raise HTTPException(
            status_code=500,
            detail="Error interno al obtener los roles"
            )
        


    def crear(self, adjudicacion: AdjudicacionModel):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO adjudicacion (
                    id_postulacion,
                    fecha_adjudicacion,
                    resultado,
                    porcentaje_aprobado,
                    monto_aprobado,
                    observaciones,
                    estado
                    
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_adjudicacion;
            """

            cursor.execute(query, (
                adjudicacion.id_postulacion,
                adjudicacion.fecha_adjudicacion,
                adjudicacion.resultado,
                adjudicacion.porcentaje_aprobado,
                adjudicacion.monto_aprobado,
                adjudicacion.observaciones,
                adjudicacion.estado
            ))

            nuevo_id = cursor.fetchone()['id_adjudicacion']

            conn.commit()
            conn.close()

            return nuevo_id
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def eliminar(self, adjudicacion_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM adjudicacion
                WHERE id_adjudicacion = %s
                RETURNING id_adjudicacion;
            """, (adjudicacion_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def actualizar(
        self,
        adjudicacion_id: int,
        adjudicacion: AdjudicacionModel
    ):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE adjudicacion
                SET
                    id_postulacion = %s,
                    fecha_adjudicacion = %s,
                    resultado = %s,
                    porcentaje_aprobado = %s,
                    monto_aprobado = %s,
                    observaciones = %s,
                    estado= %s
                WHERE id_adjudicacion = %s
                RETURNING id_adjudicacion;
            """

            cursor.execute(query, (
                adjudicacion.id_postulacion,
                adjudicacion.fecha_adjudicacion,
                adjudicacion.resultado,
                adjudicacion.porcentaje_aprobado,
                adjudicacion.monto_aprobado,
                adjudicacion.observaciones,
                adjudicacion.estado,
                adjudicacion_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None