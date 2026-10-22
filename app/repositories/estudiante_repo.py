
from app.core.database import Database
from app.models.estudiante import Estudiante


class EstudianteRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar con la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM estudiante
                ORDER BY id_estudiante ASC;
            """)

            return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener estudiantes: {e}")
            raise

        finally:
            if conn is not None:
                conn.close()

    def obtener_por_id(self, id_estudiante: int):
        conn = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar con la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM estudiante
                WHERE id_estudiante = %s;
            """, (id_estudiante,))

            return cursor.fetchone()

        except Exception as e:
            print(f"Error al obtener estudiante por ID: {e}")
            raise

        finally:
            if conn is not None:
                conn.close()

    def obtener_por_documento(self, documento: str):
        conn = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar con la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM estudiante
                WHERE documento = %s
                  AND estado = TRUE
                LIMIT 1;
            """, (documento,))

            return cursor.fetchone()

        except Exception as e:
            print(f"Error al obtener estudiante por documento: {e}")
            raise

        finally:
            if conn is not None:
                conn.close()

    def obtener_por_programa(self, id_programa: int):
        conn = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar con la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM estudiante
                WHERE id_programa = %s
                ORDER BY id_estudiante ASC;
            """, (id_programa,))

            return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener estudiantes por programa: {e}")
            raise

        finally:
            if conn is not None:
                conn.close()

    def crear(self, estudiante: Estudiante):
        conn = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar con la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO estudiante (
                    id_programa,
                    documento,
                    nombres,
                    apellidos,
                    email,
                    telefono,
                    fecha_ingreso,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_estudiante;
            """, (
                estudiante.id_programa,
                estudiante.documento,
                estudiante.nombres,
                estudiante.apellidos,
                estudiante.email,
                estudiante.telefono,
                estudiante.fecha_ingreso,
                estudiante.estado
            ))

            resultado = cursor.fetchone()
            nuevo_id = resultado["id_estudiante"]

            conn.commit()

            return nuevo_id

        except Exception as e:
            if conn is not None:
                conn.rollback()

            print(f"Error al crear estudiante: {e}")
            raise

        finally:
            if conn is not None:
                conn.close()

    def actualizar(self, id_estudiante: int, estudiante: Estudiante):
        conn = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar con la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                UPDATE estudiante
                SET
                    id_programa = %s,
                    documento = %s,
                    nombres = %s,
                    apellidos = %s,
                    email = %s,
                    telefono = %s,
                    fecha_ingreso = %s,
                    estado = %s
                WHERE id_estudiante = %s;
            """, (
                estudiante.id_programa,
                estudiante.documento,
                estudiante.nombres,
                estudiante.apellidos,
                estudiante.email,
                estudiante.telefono,
                estudiante.fecha_ingreso,
                estudiante.estado,
                id_estudiante
            ))

            actualizado = cursor.rowcount > 0

            conn.commit()

            return actualizado

        except Exception as e:
            if conn is not None:
                conn.rollback()

            print(f"Error al actualizar estudiante: {e}")
            raise

        finally:
            if conn is not None:
                conn.close()
