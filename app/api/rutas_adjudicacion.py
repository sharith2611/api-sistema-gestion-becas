from fastapi import APIRouter, HTTPException
from app.models.adjudicacion import Adjudicacion
from app.repositories.adjudicacion_repo import AdjudicacionRepository

router = APIRouter(prefix="/adjudicaciones", tags=["Adjudicacion"])

repo = AdjudicacionRepository()


@router.get("/")
def listar_adjudicaciones():
    return repo.obtener_todos()


@router.get("/{id_adjudicacion}")
def obtener_adjudicacion(id_adjudicacion: int):
    registro = repo.obtener_por_id(id_adjudicacion)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return registro


@router.post("/")
def crear_adjudicacion(adjudicacion: Adjudicacion):
    nuevo_id = repo.crear(adjudicacion)
    return {
        "mensaje": "Registro creado exitosamente",
        "id": nuevo_id
    }


@router.put("/{id_adjudicacion}")
def actualizar_adjudicacion(
    id_adjudicacion: int,
    adjudicacion: Adjudicacion
):
    exito = repo.actualizar(id_adjudicacion, adjudicacion)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro actualizado correctamente"}


@router.delete("/{id_adjudicacion}")
def eliminar_adjudicacion(id_adjudicacion: int):
    exito = repo.eliminar(id_adjudicacion)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro eliminado correctamente"}

