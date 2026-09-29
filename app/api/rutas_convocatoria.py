from fastapi import APIRouter, HTTPException
from app.models.convocatoria import Convocatoria
from app.repositories.convocatoria_repo import ConvocatoriaRepository

router = APIRouter(prefix="/convocatorias", tags=["Convocatoria"])

repo = ConvocatoriaRepository()


@router.get("/")
def listar_convocatorias():
    return repo.obtener_todos()


@router.get("/{id_convocatoria}")
def obtener_convocatoria(id_convocatoria: int):
    registro = repo.obtener_por_id(id_convocatoria)

    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return registro


@router.post("/")
def crear_convocatoria(convocatoria: Convocatoria):
    nuevo_id = repo.crear(convocatoria)

    return {
        "mensaje": "Registro creado exitosamente",
        "id": nuevo_id
    }


@router.put("/{id_convocatoria}")
def actualizar_convocatoria(id_convocatoria: int, convocatoria: Convocatoria):
    exito = repo.actualizar(id_convocatoria, convocatoria)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro actualizado correctamente"}


@router.delete("/{id_convocatoria}")
def eliminar_convocatoria(id_convocatoria: int):
    exito = repo.eliminar(id_convocatoria)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro eliminado correctamente"}

