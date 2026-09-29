from fastapi import APIRouter, HTTPException
from app.models.institucion import Institucion
from app.repositories.institucion_repo import InstitucionRepository

router = APIRouter(prefix="/instituciones", tags=["Institucion"])

repo = InstitucionRepository()


@router.get("/")
def listar_instituciones():
    return repo.obtener_todos()


@router.get("/{id_institucion}")
def obtener_institucion(id_institucion: int):
    registro = repo.obtener_por_id(id_institucion)

    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return registro


@router.post("/")
def crear_institucion(institucion: Institucion):
    nuevo_id = repo.crear(institucion)

    return {
        "mensaje": "Registro creado exitosamente",
        "id": nuevo_id
    }


@router.put("/{id_institucion}")
def actualizar_institucion(id_institucion: int, institucion: Institucion):
    exito = repo.actualizar(id_institucion, institucion)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro actualizado correctamente"}


@router.delete("/{id_institucion}")
def eliminar_institucion(id_institucion: int):
    exito = repo.eliminar(id_institucion)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro eliminado correctamente"}