
from app.core.database import Database
from app.models.documento_postulacion import DocumentoPostulacion as DocumentoPostulacionModel


class DocumentoPostulacionRepository:

    def __init__(self):
        # Composición: el repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM documento_postulacion
                ORDER BY id_documento_postulacion ASC;
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
                FROM documento_postulacion
                WHERE id_documento_postulacion = %s;
            """, (documento_id,))

            registro = cursor.fetchone()

            conn.close()
            return registro

        except Exception as e:
            print(f"Error de conexión a la BD: {e}")
            return None

    def crear(self, documento: DocumentoPostulacionModel):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO documento_postulacion (
                    id_postulacion,
                    nombre_archivo,
                    ruta_archivo,
                    fecha_carga,
                    estado,
                    observacion
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_documento_postulacion;
            """

            cursor.execute(query, (
                documento.id_postulacion,
                documento.nombre_archivo,
                documento.ruta_archivo,
                documento.fecha_carga,
                documento.estado,
                documento.observacion
            ))

            nuevo_id = cursor.fetchone()['id_documento_postulacion']

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
                DELETE FROM documento_postulacion
                WHERE id_documento_postulacion = %s
                RETURNING id_documento_postulacion;
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
        documento: DocumentoPostulacionModel
    ):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE documento_postulacion
                SET
                    id_postulacion = %s,
                    nombre_archivo = %s,
                    ruta_archivo = %s,
                    fecha_carga = %s,
                    estado = %s,
                    observacion = %s
                WHERE id_documento_postulacion = %s
                RETURNING id_documento_postulacion;
            """

            cursor.execute(query, (
                documento.id_postulacion,
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
