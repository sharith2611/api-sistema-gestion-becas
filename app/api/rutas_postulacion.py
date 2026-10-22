
from fastapi import APIRouter, HTTPException

from app.models.postulacion import Postulacion
from app.repositories.postulacion_repo import PostulacionRepository


router = APIRouter(
    prefix="/postulaciones",
    tags=["Postulaciones"]
)

repo = PostulacionRepository()


@router.get("/")
def listar_postulaciones():
    registros = repo.obtenertodos_estudiantes()

    if registros is None:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar las postulaciones"
        )

    return registros


@router.get("/{id_postulacion}")
def obtener_postulacion(id_postulacion: int):
    registro = repo.obtener_por_id(id_postulacion)

    if not registro:
        raise HTTPException(
            status_code=404,
            detail="Postulación no encontrada"
        )

    return registro


@router.post("/")
def crear_postulacion(postulacion: Postulacion):
    nuevo_id = repo.crear(postulacion)

    if nuevo_id is None:
        raise HTTPException(
            status_code=500,
            detail="Error al crear la postulación"
        )

    return {
        "mensaje": "Postulación creada exitosamente",
        "id": nuevo_id
    }


@router.put("/{id_postulacion}")
def actualizar_postulacion(
    id_postulacion: int,
    postulacion: Postulacion
):
    exito = repo.actualizar(
        id_postulacion,
        postulacion
    )

    if exito is None:
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar la postulación"
        )

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Postulación no encontrada"
        )

    return {
        "mensaje": "Postulación actualizada correctamente"
    }


@router.delete("/{id_postulacion}")
def eliminar_postulacion(id_postulacion: int):
    exito = repo.eliminar(id_postulacion)

    if exito is None:
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar la postulación"
        )

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Postulación no encontrada"
        )

    return {
        "mensaje": "Postulación eliminada correctamente"
    }


@router.get("/convocatoria/{id_convocatoria}")
def obtener_por_convocatoria(id_convocatoria: int):
    return repo.obtener_por_convocatoria(id_convocatoria)


@router.get("/estudiante/{id_estudiante}")
def obtener_por_estudiante(id_estudiante: int):
    return repo.obtener_por_estudiante(id_estudiante)
