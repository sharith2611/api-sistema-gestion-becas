from fastapi import APIRouter, HTTPException
from app.models.documento_adjudicacion import DocumentoAdjudicacion
from app.repositories.documento_adjudicacion_repo import DocumentoAdjudicacionRepository
router = APIRouter(prefix="/documentoAdjudicacion", tags=["DocumentoAdjudicacion"])

repo = DocumentoAdjudicacionRepository()


@router.get("/")
def listar_documento_adjudicacion():
    return repo.obtener_todos()


@router.get("/{id_documento_adjudicacion}")
def obtener_documento_adjudicacion(id_documento_adjudicacion: int):
    registro = repo.obtener_por_id(id_documento_adjudicacion)

    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return registro


@router.post("/")
def crear_documento_adjudicacion(documentoAdjudicacion: DocumentoAdjudicacion):
    nuevo_id = repo.crear(documentoAdjudicacion)

    return {
        "mensaje": "Registro creado exitosamente",
        "id": nuevo_id
    }


@router.put("/{id_convocatoria}")
def actualizar_documento_adjudicacion(id_documento_adjudicacion: int, documentoAdjudicacion: DocumentoAdjudicacion):
    exito = repo.actualizar(id_documento_adjudicacion, documentoAdjudicacion)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro actualizado correctamente"}


@router.delete("/{id_convocatoria}")
def eliminar_documento_adjudicacion(id_documento_adjudicacion: int):
    exito = repo.eliminar(id_documento_adjudicacion)

    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"mensaje": "Registro eliminado correctamente"}

