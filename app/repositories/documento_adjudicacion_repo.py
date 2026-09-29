from app.core.database import Database
from app.models.documento_adjudicacion import DocumentoAdjudicacion as DocumentoAdjudicacionModel
from fastapi import APIRouter, HTTPException



class DocumentoAdjudicacionRepository:

    def __init__(self):
        # Composición: el repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM documento_adjudicacion
                ORDER BY id_documento_adjudicacion ASC;
            """)

            registros = cursor.fetchall()

            conn.close()
            return registros
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def obtener_por_id(self, documento_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM documento_adjudicacion
                WHERE id_documento_adjudicacion = %s;
            """, (documento_id,))

            registro = cursor.fetchone()

            conn.close()
            return registro
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None
                
    def crear(self, documento: DocumentoAdjudicacionModel):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO documento_adjudicacion (
                    id_adjudicacion,
                    nombre_archivo,
                    ruta_archivo,
                    fecha_carga,
                    estado,
                    observacion
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_documento_adjudicacion;
            """

            cursor.execute(query, (
                documento.id_documento_adjudicacion,
                documento.nombre_archivo,
                documento.ruta_archivo,
                documento.fecha_carga,
                documento.estado,
                documento.observacion
            ))

            nuevo_id = cursor.fetchone()['id_documento_adjudicacion']

            conn.commit()
            conn.close()

            return nuevo_id
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None
                
    def eliminar(self, documento_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM documento_adjudicacion
                WHERE id_documento_adjudicacion = %s
                RETURNING id_documento_adjudicacion;
            """, (documento_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def actualizar(
        self,
        documento_id: int,
        documento: DocumentoAdjudicacionModel
    ):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE documento_adjudicacion
                SET
                    id_adjudicacion = %s,
                    nombre_archivo = %s,
                    ruta_archivo = %s,
                    fecha_carga = %s,
                    estado = %s,
                    observacion = %s
                WHERE id_documento_adjudicacion = %s
                RETURNING id_documento_adjudicacion;
            """

            cursor.execute(query, (
                documento.id_adjudicacion,
                documento.nombre_archivo,
                documento.ruta_archivo,
                documento.fecha_carga,
                documento.estado,
                documento.observacion,
                documento_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None 
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None