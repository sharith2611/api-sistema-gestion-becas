
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
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    return registro


@router.post("/")
def crear_estudiante(estudiante: Estudiante):
    nuevo_id = repo.crear(estudiante)

    if nuevo_id is None:
        raise HTTPException(
            status_code=500,
            detail="No fue posible registrar el estudiante"
        )

    return {
        "mensaje": "Registro creado exitosamente",
        "id": nuevo_id
    }


@router.put("/{id_estudiante}")
def actualizar_estudiante(
    id_estudiante: int,
    estudiante: Estudiante
):
    exito = repo.actualizar(id_estudiante, estudiante)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado o no se pudo actualizar"
        )

    return {
        "mensaje": "Registro actualizado correctamente"
    }


@router.get("/documento/{documento}")
def obtener_estudiante_por_documento(documento: str):
    estudiante = repo.obtener_por_documento(documento)

    if not estudiante:
        raise HTTPException(
            status_code=404,
            detail="No existe un estudiante registrado con esa cédula."
        )

    return estudiante
