from app.core.database import Database
from app.models.auxilio_educativo import  auxilio_educativo as AuxilioEducativoModel
from fastapi import APIRouter, HTTPException




class AuxilioEducativoRepository:

    def __init__(self):
        # Composición: el repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM auxilio_educativo
                ORDER BY id_auxilio ASC;
            """)

            registros = cursor.fetchall()

            conn.close()
            return registros
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None
        


    def obtener_por_id(self, auxilio_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM auxilio_educativo
                WHERE id_auxilio = %s;
            """, (auxilio_id,))

            registro = cursor.fetchone()

            conn.close()
            return registro
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def crear(self, auxilio: AuxilioEducativoModel):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO auxilio_educativo (
                    id_facultad,
                    nombre,
                    descripcion,
                    porcentaje_maximo,
                    monto_maximo,
                    estado,
                    tipo_auxilio
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_auxilio;
            """

            cursor.execute(query, (
                auxilio.id_facultad,
                auxilio.nombre,
                auxilio.descripcion,
                auxilio.porcentaje_maximo,
                auxilio.monto_maximo,
                auxilio.estado,
                auxilio.tipo_auxilio
            ))

            nuevo_id = cursor.fetchone()['id_auxilio']

            conn.commit()
            conn.close()

            return nuevo_id
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None
                
    def eliminar(self, auxilio_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM auxilio_educativo
                WHERE id_auxilio = %s
                RETURNING id_auxilio;
            """, (auxilio_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def actualizar(
        self,
        auxilio_id: int,
        auxilio: AuxilioEducativoModel
    ):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE auxilio_educativo
                SET
                    id_facultad = %s,
                    nombre = %s,
                    descripcion = %s,
                    porcentaje_maximo = %s,
                    monto_maximo = %s,
                    estado = %s,
                    tipo_auxilio = %s
                WHERE id_auxilio = %s
                RETURNING id_auxilio;
            """

            cursor.execute(query, (
                auxilio.id_facultad,
                auxilio.nombre,
                auxilio.descripcion,
                auxilio.porcentaje_maximo,
                auxilio.monto_maximo,
                auxilio.estado,
                auxilio.tipo_auxilio,
                auxilio_id
            ))

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None