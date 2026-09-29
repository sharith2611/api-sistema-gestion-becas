from app.core.database import Database
from app.models.rol import Rol
from fastapi import APIRouter, HTTPException

class RolRepository:
     
    def __init__(self):
        self.db = Database()

    
    
    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM rol
                ORDER BY id_rol ASC;
            """)

            usuarios = cursor.fetchall()

            conn.close()

            return usuarios
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None
                
    def obtener_por_id(self, usuario_id: int):
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM rol
                WHERE id_rol = %s;
            """, (usuario_id,))

            usuario = cursor.fetchone()

            conn.close()

            return usuario
    
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None
 

    def crear(self, rol: Rol):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO rol
                (id_rol, descripcion, estado)
                VALUES (%s, %s, %s)
                RETURNING id_rol;
                """

            cursor.execute(
                query,
                (
                    rol.id_rol,
                    rol.descripcion,
                    rol.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_rol"]

            conn.commit()
            conn.close()
            return nuevo_id
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None        

    def eliminar(self, rol_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM rol
                WHERE id_usuario = %s
                RETURNING id_rol;
            """, (rol_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            return eliminado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None
            
                
    def actualizar(self, rol_id: int, rol: Rol):
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE rol
                SET descripcion = %s,
                    estado = %s
                WHERE id_rol = %s
                RETURNING id_usuario;
            """

            cursor.execute(
                query,
                (
                    rol.descripcion,
                    rol.estado,
                    rol_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            return actualizado is not None
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None
                    