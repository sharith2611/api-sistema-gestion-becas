
from app.core.database import Database
from app.models.postulacion import Postulacion
from fastapi import APIRouter, HTTPException


class PostulacionRepository:
    def __init__(self):
        # Composición: el repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM postulacion
                ORDER BY id_postulacion ASC;
            """)

            registros = cursor.fetchall()
            cursor.close()
            conn.close()

            return registros

        except Exception as e:
            print(f"Error de conexión a la BD: {e}")
            return None

    def obtenertodos_estudiantes(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                SELECT
                    p.id_postulacion,
                    p.id_estudiante,
                    e.nombres,
                    e.apellidos,
                    p.id_convocatoria,
                    p.fecha_postulacion,
                    p.observaciones,
                    p.adjuntos,
                    p.estado,
                    p.escala
                FROM postulacion p
                INNER JOIN estudiante e
                    ON p.id_estudiante = e.id_estudiante
                ORDER BY p.id_postulacion ASC;
            """

            cursor.execute(query)
            registros = cursor.fetchall()

            cursor.close()
            conn.close()

            return registros

        except Exception as e:
            print(f"Error al consultar las postulaciones con estudiantes: {e}")
            return None

    def obtener_por_id(self, id_postulacion: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM postulacion WHERE id_postulacion = %s;",
                (id_postulacion,)
            )

            registro = cursor.fetchone()

            cursor.close()
            conn.close()

            return registro

        except Exception as e:
            print(f"Error de conexión a la BD: {e}")
            return None

    def crear(self, postulacion: Postulacion):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO postulacion (
                    id_estudiante,
                    id_convocatoria,
                    fecha_postulacion,
                    observaciones,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_postulacion;
            """

            cursor.execute(query, (
                postulacion.id_estudiante,
                postulacion.id_convocatoria,
                postulacion.fecha_postulacion,
                postulacion.observaciones,
                postulacion.estado
            ))

            nuevo_id = cursor.fetchone()['id_postulacion']

            conn.commit()
            cursor.close()
            conn.close()

            return nuevo_id

        except Exception as e:
            print(f"Error de conexión a la BD: {e}")
            return None

    def eliminar(self, id_postulacion: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM postulacion
                WHERE id_postulacion = %s
                RETURNING id_postulacion;
                """,
                (id_postulacion,)
            )

            eliminado = cursor.fetchone()

            conn.commit()
            cursor.close()
            conn.close()

            return eliminado is not None

        except Exception as e:
            print(f"Error de conexión a la BD: {e}")
            return None

    def actualizar(self, id_postulacion: int, postulacion: Postulacion):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE postulacion
                SET id_estudiante = %s,
                    id_convocatoria = %s,
                    fecha_postulacion = %s,
                    estado = %s,
                    observaciones = %s,
                    adjuntos = %s,
                    escala = %s
                WHERE id_postulacion = %s
                RETURNING id_postulacion;
            """

            cursor.execute(query, (
                postulacion.id_estudiante,
                postulacion.id_convocatoria,
                postulacion.fecha_postulacion,
                postulacion.estado,
                postulacion.observaciones,
                postulacion.adjuntos,
                postulacion.escala,
                id_postulacion
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            cursor.close()
            conn.close()

            return actualizado is not None

        except Exception as e:
            print(f"Error de conexión a la BD: {e}")
            return None
# ============================================================
# OBTENER TOTAL DE POSTULACIONES
# ============================================================
    def obtener_total_postulaciones(self):
        conn = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar con la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM postulacion
            """)

            registro = cursor.fetchone()

            return registro["total"]

        except Exception as e:
            print(f"Error al obtener total de postulaciones: {e}")
            raise

        finally:
            if conn is not None:
                conn.close()
                
    # ============================================================
    # OBTENER ÚLTIMAS POSTULACIONES
    # ============================================================
    def obtener_ultimas_postulaciones(self):
        conn = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar con la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    e.nombres || ' ' || e.apellidos AS estudiante,
                    c.nombre AS convocatoria,
                    p.fecha_postulacion AS fecha,
                    p.estado
                FROM postulacion p
                INNER JOIN estudiante e
                    ON p.id_estudiante = e.id_estudiante
                INNER JOIN convocatoria c
                    ON p.id_convocatoria = c.id_convocatoria
                ORDER BY p.fecha_postulacion DESC
                LIMIT 5
            """)

            registros = cursor.fetchall()

            return registros

        except Exception as e:
            print(f"Error al obtener últimas postulaciones: {e}")
            raise

        finally:
            if conn is not None:
                conn.close()
                
    # ============================================================
    # OBTENER POSTULACIONES POR ESTADO
    # ============================================================
    def obtener_postulaciones_por_estado(self):
        conn = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar con la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    estado,
                    COUNT(*) AS cantidad
                FROM postulacion
                GROUP BY estado
                ORDER BY cantidad DESC
            """)

            registros = cursor.fetchall()

            return registros

        except Exception as e:
            print(f"Error al obtener postulaciones por estado: {e}")
            raise

        finally:
            if conn is not None:
                conn.close()

    def obtener_postulaciones_por_auxilio(self):
        conn = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar con la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    a.nombre AS auxilio,
                    COUNT(p.id_postulacion) AS cantidad
                FROM auxilio_educativo a
                INNER JOIN convocatoria c
                    ON a.id_auxilio = c.id_auxilio
                INNER JOIN postulacion p
                    ON c.id_convocatoria = p.id_convocatoria
                GROUP BY a.id_auxilio, a.nombre
                ORDER BY cantidad DESC
            """)

            registros = cursor.fetchall()
            return registros

        except Exception as e:
            print(f"Error al obtener postulaciones por auxilio: {e}")
            raise

        finally:
            if conn is not None:
                conn.close()
    def obtener_datos_tablero(self):
        conn = None
        try:
            conn = self.db.get_connection()
            if conn is None:
                raise Exception("No se pudo conectar con la base de datos.")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    p.id_estudiante,
                    p.id_convocatoria,
                    e.nombres || ' ' || e.apellidos AS estudiante,
                    c.nombre AS convocatoria,
                    ae.nombre AS auxilio,
                    p.fecha_postulacion AS fecha,
                    p.estado,
                    COALESCE(adj.cantidad_adjudicaciones, 0) AS cantidad_adjudicaciones
                FROM postulacion p
                INNER JOIN estudiante e
                    ON e.id_estudiante = p.id_estudiante
                INNER JOIN convocatoria c
                    ON c.id_convocatoria = p.id_convocatoria
                INNER JOIN auxilio_educativo ae
                    ON ae.id_auxilio = c.id_auxilio
                LEFT JOIN LATERAL (
                    SELECT COUNT(*) AS cantidad_adjudicaciones
                    FROM adjudicacion a
                    WHERE a.id_postulacion = p.id_postulacion
                ) adj ON TRUE
                ORDER BY p.fecha_postulacion DESC, p.id_postulacion DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al consultar los datos del tablero: {e}")
            raise
        finally:
            if conn is not None:
                conn.close()
                
                
# ============================================================
# OBTENER POSTULACIONES AGRUPADAS POR ESCALA
# ============================================================
    def obtener_postulaciones_por_escala(self):
        conn = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar con la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    escala,
                    COUNT(*) AS cantidad
                FROM postulacion
                GROUP BY escala
                ORDER BY cantidad DESC
            """)

            return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener postulaciones por escala: {e}")
            raise

        finally:
            if conn is not None:
                conn.close()
