from fastapi import APIRouter, HTTPException
from app.models.requisito_convocatoria import RequisitoConvocatoria
from app.repositories.requisito_convocatoria import RequisitoConvocatoriaRepository

router = APIRouter(
    prefix="/requisitos-convocatoria",
    tags=["Requisito Convocatoria"]
)

repo = RequisitoConvocatoriaRepository()


@router.get("/")
def listar_requisitos():
    return repo.obtener_todos()


@router.get("/{id_requisito_convocatoria}")
def obtener_requisito(id_requisito_convocatoria: int):
    registro = repo.obtener_por_id(id_requisito_convocatoria)

    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return registro


@router.post("/")
def crear_requisito(requisito: RequisitoConvocatoria):
    nuevo_id = repo.crear(requisito)

    return {
        "mensaje": "Registro creado exitosamente",
        "id": nuevo_id
    }


@router.put("/{id_requisito_convocatoria}")
def actualizar_requisito(
    id_requisito_convocatoria: int,
    requisito: RequisitoConvocatoria
):
    exito = repo.actualizar(id_requisito_convocatoria, requisito)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro actualizado correctamente"}


@router.delete("/{id_requisito_convocatoria}")
def eliminar_requisito(id_requisito_convocatoria: int):
    exito = repo.eliminar(id_requisito_convocatoria)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro eliminado correctamente"}

