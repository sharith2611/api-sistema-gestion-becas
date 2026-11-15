from app.core.database import Database


class ReporteRepository:
    def __init__(self):
        self.db = Database()

    def obtener_convocatorias(self):
        conn = self.db.get_connection()
        if conn is None:
            raise RuntimeError('No fue posible conectar con la base de datos')
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    SELECT id_convocatoria, nombre
                    FROM public.convocatoria
                    ORDER BY nombre, id_convocatoria
                ''')
                return [dict(fila) for fila in cursor.fetchall()]
        finally:
            conn.close()

    def obtener_escalas(self):
        conn = self.db.get_connection()
        if conn is None:
            raise RuntimeError('No fue posible conectar con la base de datos')
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    SELECT DISTINCT escala
                    FROM public.postulacion
                    WHERE escala IS NOT NULL AND TRIM(escala) <> ''
                    ORDER BY escala
                ''')
                return [fila['escala'] for fila in cursor.fetchall()]
        finally:
            conn.close()

    def consultar(self, fecha_inicio=None, fecha_fin=None, escala=None, id_convocatoria=None):
        conn = self.db.get_connection()
        if conn is None:
            raise RuntimeError('No fue posible conectar con la base de datos')
        try:
            with conn.cursor() as cursor:
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
                    JOIN public.programa_academico pa ON pa.id_programa = e.id_programa
                    JOIN public.facultad f ON f.id_facultad = pa.id_facultad
                    JOIN public.institucion i ON i.id_institucion = f.id_institucion
                    JOIN public.convocatoria c ON c.id_convocatoria = p.id_convocatoria
                    JOIN public.auxilio_educativo ae ON ae.id_auxilio = c.id_auxilio
                    WHERE (%s::date IS NULL OR p.fecha_postulacion >= %s::date)
                      AND (%s::date IS NULL OR p.fecha_postulacion < %s::date + INTERVAL '1 day')
                      AND (%s::text IS NULL OR p.escala = %s::text)
                      AND (%s::integer IS NULL OR c.id_convocatoria = %s::integer)
                    ORDER BY p.fecha_postulacion DESC, e.apellidos, e.nombres
                ''', (
                    fecha_inicio, fecha_inicio,
                    fecha_fin, fecha_fin,
                    escala, escala,
                    id_convocatoria, id_convocatoria,
                ))
                return [dict(fila) for fila in cursor.fetchall()]
        finally:
            conn.close()


    def obtener_programas(self):
        conn = self.db.get_connection()
        if conn is None:
            raise RuntimeError('No fue posible conectar con la base de datos')
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    SELECT id_programa, nombre
                    FROM public.programa_academico
                    ORDER BY nombre, id_programa
                ''')
                return [dict(fila) for fila in cursor.fetchall()]
        finally:
            conn.close()

    def consultar_estudiantes(self, fecha_inicio=None, fecha_fin=None,
                            id_programa=None, estado_estudiante=None):
        conn = self.db.get_connection()
        if conn is None:
            raise RuntimeError('No fue posible conectar con la base de datos')
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    SELECT
                        CONCAT_WS(' ', e.nombres, e.apellidos) AS estudiante,
                        e.email AS correo,
                        e.telefono AS telefono,
                        i.nombre AS institucion,
                        f.nombre AS facultad,
                        pa.nombre AS programa,
                        TO_CHAR(e.fecha_ingreso, 'DD/MM/YYYY') AS fecha,
                        CASE WHEN e.estado THEN 'Activo' ELSE 'Inactivo' END AS estado_estudiante
                    FROM public.estudiante e
                    JOIN public.programa_academico pa ON pa.id_programa = e.id_programa
                    JOIN public.facultad f ON f.id_facultad = pa.id_facultad
                    JOIN public.institucion i ON i.id_institucion = f.id_institucion
                    WHERE (%s::date IS NULL OR e.fecha_ingreso >= %s::date)
                    AND (%s::date IS NULL OR e.fecha_ingreso <= %s::date)
                    AND (%s::integer IS NULL OR e.id_programa = %s::integer)
                    AND (%s::boolean IS NULL OR e.estado = %s::boolean)
                    ORDER BY e.apellidos, e.nombres
                ''', (
                    fecha_inicio, fecha_inicio,
                    fecha_fin, fecha_fin,
                    id_programa, id_programa,
                    estado_estudiante, estado_estudiante,
                ))
                return [dict(fila) for fila in cursor.fetchall()]
        finally:
            conn.close()
