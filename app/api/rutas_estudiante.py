from fastapi import APIRouter, HTTPException
from app.models.estudiante import Estudiante
from app.repositories.estudiante_repo import EstudianteRepository

router = APIRouter(prefix="/estudiantes", tags=["Estudiante"])

repo = EstudianteRepository()


@router.get("/")
def listar_estudiantes():
    return repo.obtener_todos()


@router.get("/{id_estudiante}")
def obtener_estudiante(id_estudiante: int):
    registro = repo.obtener_por_id(id_estudiante)

    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return registro


@router.post("/")
def crear_estudiante(estudiante: Estudiante):
    nuevo_id = repo.crear(estudiante)

    return {"mensaje": "Registro creado exitosamente", "id": nuevo_id}


@router.put("/{id_estudiante}")
def actualizar_estudiante(id_estudiante: int, estudiante: Estudiante):
    exito = repo.actualizar(id_estudiante, estudiante)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro actualizado correctamente"}


@router.delete("/{id_estudiante}")
def eliminar_estudiante(id_estudiante: int):
    exito = repo.eliminar(id_estudiante)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro eliminado correctamente"}


