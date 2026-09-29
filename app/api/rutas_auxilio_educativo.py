from fastapi import APIRouter, HTTPException
from app.models.auxilio_educativo import auxilio_educativo
from app.repositories.auxilio_educativo_repo import AuxilioEducativoRepository

router = APIRouter(prefix="/auxilio_educativo", tags=["auxilio_educativo"])

repo = AuxilioEducativoRepository()

@router.get("/")
def listar_auxlio_educativo():
    return repo.obtener_todos()

@router.get("/{id_auxilio_educativo}")
def obtener_auxilio_educativo(id_auxilio_educativo: int):
    registro = repo.obtener_por_id(id_auxilio_educativo)

    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return registro

@router.post("/")
def crear_auxilio_educativo(auxilio_educativo: auxilio_educativo):
    nuevo_id = repo.crear(auxilio_educativo)

    return {"mensaje": "Registro creado exitosamente", "id": nuevo_id}

@router.put("/{id_beca}")
def actualizar_auxilio_educativo(id_auxilio_educativo: int, auxilio_educativo: auxilio_educativo):
    exito = repo.actualizar(id_auxilio_educativo, auxilio_educativo)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro actualizado correctamente"}

@router.delete("/{id_auxilio_educativo}")
def eliminar_auxilio_educativo(id_auxilio_educativo: int):
    exito = repo.eliminar(id_auxilio_educativo)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro eliminado correctamente"}