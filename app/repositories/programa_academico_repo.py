from app.core.database import Database
from app.models.programa_academico import ProgramaAcademico
from fastapi import APIRouter, HTTPException


class ProgramaAcademicoRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM programa_academico ORDER BY id_programa ASC;"
            )

            registros = cursor.fetchall()
            conn.close()

            return registros
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def obtener_por_id(self, id_programa: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM programa_academico WHERE id_programa=%s;",
                (id_programa,)
            )

            registro = cursor.fetchone()

            conn.close()

            return registro
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def obtener_por_institucion(self, id_institucion: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM programa_academico WHERE id_institucion=%s;",
                (id_institucion,)
            )

            registros = cursor.fetchall()

            conn.close()

            return registros
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None

    def crear(self, programa: ProgramaAcademico):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO programa_academico
            (id_facultad,codigo,nombre,nivel,modalidad,estado)
            VALUES (%s,%s,%s,%s,%s,%s)
            RETURNING id_programa;
            """

            cursor.execute(query, (
                programa.id_facultad,
                programa.codigo,
                programa.nombre,
                programa.nivel,
                programa.modalidad,
                programa.estado
            ))

            nuevo_id = cursor.fetchone()["id_programa"]

            conn.commit()
            conn.close()

            return nuevo_id
        except Exception as e:
                    print(f"Error de conexión a la BD: {e}")
                    return None


    
    def actualizar(self, id_programa: int, programa: ProgramaAcademico):
            try:    
                conn = self.db.get_connection()
                cursor = conn.cursor()
    
    
   
                query = """
                    UPDATE programa_academico
                    SET id_facultad = %s,
                        codigo = %s,
                        nombre = %s,
                        nivel = %s,
                        modalidad=%s,
                        estado=%s
                    WHERE id_requisito_convocatoria = %s
                    RETURNING id_programa_academico;
                """
    
    
                cursor.execute(query, (
                    programa.id_facultad,
                    programa.codigo,
                    programa.nombre,
                    programa.nivel,
                    programa.modalidad,
                    id_programa
                ))
    
                actualizado = cursor.fetchone()
    
                conn.commit()
                conn.close()
    
                return actualizado is not None
            except Exception as e:
                        print(f"Error de conexión a la BD: {e}")
                        return None

    def eliminar(self, id_programa: int):
        pass