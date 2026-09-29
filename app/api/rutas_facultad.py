from fastapi import APIRouter, HTTPException
from app.models.facultad import Facultad
from app.repositories.facultad_repo import FacultadRepository

router = APIRouter(prefix="/facultad", tags=["Facultad"])

repo = FacultadRepository()


@router.get("/")
def listar_facultad():
    return repo.obtener_todos()


@router.get("/{id_facultad}")
def obtener_facultad(id_facultad: int):
    registro = repo.obtener_por_id(id_facultad)

    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return registro


@router.post("/")
def crear_facultad(facultad: Facultad):
    nuevo_id = repo.crear(facultad)

    return {"mensaje": "Registro creado exitosamente", "id": nuevo_id}


@router.put("/{id_facultad}")
def actualizar_facultad(id_facultad: int, facultad: Facultad):
    exito = repo.actualizar(id_facultad, facultad)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro actualizado correctamente"}


@router.delete("/{id_facultad}")
def eliminar_facultad(id_facultad: int):
    exito = repo.eliminar(id_facultad)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro eliminado correctamente"}


