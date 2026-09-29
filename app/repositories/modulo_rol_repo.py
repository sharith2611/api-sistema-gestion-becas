from app.core.database import Database
from app.models.modulo_rol import ModuloRol
from fastapi import APIRouter, HTTPException


class ModuloRolRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):   
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulo_rol
                ORDER BY id_modulo_rol ASC;
            """)

            registros = cursor.fetchall()

            conn.close()

            return registros
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def obtener_por_id(self, modulo_rol_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulo_rol
                WHERE id_modulo_rol = %s;
            """, (modulo_rol_id,))

            registro = cursor.fetchone()

            conn.close()

            return registro
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None
                
                
    def crear(self, modulo_rol: ModuloRol):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO modulo_rol
                (id_modulo_rol, id_modulo, id_usuario,estado)
                VALUES (%s, %s, %s,%s)
                RETURNING id_modulo_rol;
            """

            cursor.execute(
                query,
                (
                    modulo_rol.id_modulo_rol,
                    modulo_rol.id_modulo,
                    modulo_rol.estado,
                    modulo_rol.id_usuario
                )
            )

            nuevo_id = cursor.fetchone()["id_modulo_rol"]

            conn.commit()
            conn.close()

            return nuevo_id
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None
        

    def eliminar(self, modulo_rol_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM modulo_rol
                WHERE id_modulo_rol = %s
                RETURNING id_modulo_rol;
            """, (modulo_rol_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def actualizar(self, modulo_rol_id: int, modulo_rol: ModuloRol):
        try:    
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE modulo_rol
                SET id_modulo = %s,
                    id_usuario = %s,
                    estado=%s
                WHERE id_modulo_rol = %s
                RETURNING id_modulo_rol;
            """

            cursor.execute(
                query,
                (
                    modulo_rol.id_modulo,
                    modulo_rol.id_usuario,
                     modulo_rol.estado,
                    modulo_rol_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None