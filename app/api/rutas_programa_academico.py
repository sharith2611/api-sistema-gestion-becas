from fastapi import APIRouter, HTTPException
from app.models.programa_academico import ProgramaAcademico
from app.repositories.programa_academico_repo import ProgramaAcademicoRepository

router = APIRouter(prefix="/programas", tags=["ProgramaAcademico"])

repo = ProgramaAcademicoRepository()


@router.get("/")
def listar_programas():
    return repo.obtener_todos()


@router.get("/{id_programa}")
def obtener_programa(id_programa: int):
    registro = repo.obtener_por_id(id_programa)

    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return registro


@router.post("/")
def crear_programa(programa: ProgramaAcademico):
    nuevo_id = repo.crear(programa)

    return {"mensaje": "Registro creado exitosamente", "id": nuevo_id}


@router.put("/{id_programa}")
def actualizar_programa(id_programa: int, programa: ProgramaAcademico):
    exito = repo.actualizar(id_programa, programa)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro actualizado correctamente"}


@router.delete("/{id_programa}")
def eliminar_programa(id_programa: int):
    exito = repo.eliminar(id_programa)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro eliminado correctamente"}

