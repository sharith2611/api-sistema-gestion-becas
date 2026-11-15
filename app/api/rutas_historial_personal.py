import io

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.repositories.historial_repo import HistorialPersonalRepository
from app.api.rutas_reporte import crear_pdf, crear_excel

router = APIRouter(
    prefix="/postulaciones/mi-historial",
    tags=["Mi historial de postulaciones"]
)

repo = HistorialPersonalRepository()


def obtener_registros(id_usuario: int):
    registros = repo.consultar_por_usuario_id(id_usuario)

    if not registros:
        raise HTTPException(
            status_code=404,
            detail="No tienes postulaciones registradas."
        )

    return registros


@router.get("/pdf/")
def historial_pdf(id_usuario: int):
    registros = obtener_registros(id_usuario)
    archivo = crear_pdf(registros, tipo="postulaciones")

    return StreamingResponse(
        io.BytesIO(archivo),
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                'attachment; filename="mi_historial_postulaciones.pdf"'
        }
    )


@router.get("/excel/")
def historial_excel(id_usuario: int):
    registros = obtener_registros(id_usuario)
    archivo = crear_excel(registros, tipo="postulaciones")

    return StreamingResponse(
        io.BytesIO(archivo),
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition":
                'attachment; filename="mi_historial_postulaciones.xlsx"'
        }
    )