from app.core.database import Database
from app.models.postulacion import Postulacion
from fastapi import APIRouter, HTTPException




class PostulacionRepository:
    def __init__(self):
        # Composicion: el repositorio instancia su propia conexion
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM postulacion ORDER BY id_postulacion ASC;")
            registros = cursor.fetchall()
            conn.close()
            return registros
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def obtener_por_id(self, id_postulacion: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM postulacion WHERE id_postulacion = %s;", (sensor_id,))
            registro = cursor.fetchone()
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
                INSERT INTO postulacion (id_postulacion, id_estudiante, id_convocatoria, fecha_postulacion, observacion,estado)
                VALUES (%s, %s, %s, %s, %s,%s) RETURNING id_postulacion;
            """
            cursor.execute(query, (postulacion.id_postulacion, postulacion.id_estudiante,postulacion.id_convocatoria, postulacion.fecha_postulacion, postulacion.observaciones,postulacion.estado, ))
            nuevo_id = cursor.fetchone()['id_postulacion']
            conn.commit()
            conn.close()
            return nuevo_id
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None
                
                
                
    def eliminar(self, id_postulacion: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM postulacion WHERE id_postulacion = %s RETURNING id_postulacion;", (id_postulacion,))
            eliminado = cursor.fetchone()
            conn.commit()
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
                SET id_estudiante = %s, id_convocatoria = %s, facha_postulacion = %s, estado = %s, observacion = %s, adjuntos=%s,estado=%s
                WHERE id_postulacion = %s
                RETURNING id_postulacion;
            """
            cursor.execute(query, (postulacion.id_estudiante, postulacion.id_convocatoria, postulacion.fecha_postulacion, postulacion.estado, postulacion.observaciones, postulacion.adjuntos,postulacion.estado,postulacion.id_postulacion))
            actualizado = cursor.fetchone()
            conn.commit()
            conn.close()
            return actualizado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None