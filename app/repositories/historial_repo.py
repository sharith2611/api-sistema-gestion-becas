from app.core.database import Database


class HistorialPersonalRepository:
    def __init__(self):
        self.db = Database()

    def consultar_por_usuario_id(self, id_usuario: int):
        """Identifica al estudiante por el usuario autenticado y activo."""
        conexion = self.db.get_connection()
        if conexion is None:
            raise RuntimeError('No fue posible conectar con la base de datos')
        try:
            with conexion.cursor() as cursor:
                cursor.execute('''
                    SELECT
                        CONCAT_WS(' ', e.nombres, e.apellidos) AS estudiante,
                        i.nombre AS institucion,
                        f.nombre AS facultad,
                        pa.nombre AS programa,
                        c.nombre AS convocatoria,
                        ae.nombre AS auxilio,
                        TO_CHAR(p.fecha_postulacion, 'DD/MM/YYYY') AS fecha,
                        p.escala AS escala
                    FROM public.postulacion p
                    JOIN public.estudiante e ON e.id_estudiante = p.id_estudiante
                    JOIN public.usuario u ON u.cedula = e.documento
                    JOIN public.programa_academico pa ON pa.id_programa = e.id_programa
                    JOIN public.facultad f ON f.id_facultad = pa.id_facultad
                    JOIN public.institucion i ON i.id_institucion = f.id_institucion
                    JOIN public.convocatoria c ON c.id_convocatoria = p.id_convocatoria
                    JOIN public.auxilio_educativo ae ON ae.id_auxilio = c.id_auxilio
                    WHERE u.id_usuario = %s AND u.estado = TRUE
                    ORDER BY p.fecha_postulacion DESC, p.id_postulacion DESC
                ''', (id_usuario,))
                return [dict(fila) for fila in cursor.fetchall()]
        finally:
            conexion.close()
