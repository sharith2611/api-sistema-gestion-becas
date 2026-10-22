
from fastapi import APIRouter, HTTPException
from app.models.documento_postulacion import DocumentoPostulacion
from app.repositories.documento_postulacion_repo import DocumentoPostulacionRepository

router = APIRouter(
    prefix="/documentoPostulacion",
    tags=["DocumentoPostulacion"]
)

repo = DocumentoPostulacionRepository()


@router.get("/")
def listar_documento_postulacion():
    registros = repo.obtener_todos()

    if registros is None:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar los documentos de postulación"
        )

    return registros


@router.get("/{id_documento_postulacion}")
def obtener_documento_postulacion(id_documento_postulacion: int):
    registro = repo.obtener_por_id(id_documento_postulacion)

    if not registro:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    return registro


@router.post("/")
def crear_documento_postulacion(
    documentoPostulacion: DocumentoPostulacion
):
    nuevo_id = repo.crear(documentoPostulacion)

    if nuevo_id is None:
        raise HTTPException(
            status_code=500,
            detail="Error al crear el documento de postulación"
        )

    return {
        "mensaje": "Registro creado exitosamente",
        "id": nuevo_id
    }


@router.put("/{id_documento_postulacion}")
def actualizar_documento_postulacion(
    id_documento_postulacion: int,
    documentoPostulacion: DocumentoPostulacion
):
    exito = repo.actualizar(
        id_documento_postulacion,
        documentoPostulacion
    )

    if exito is None:
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar el documento de postulación"
        )

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    return {
        "mensaje": "Registro actualizado correctamente"
    }


@router.delete("/{id_documento_postulacion}")
def eliminar_documento_postulacion(
    id_documento_postulacion: int
):
    exito = repo.eliminar(id_documento_postulacion)

    if exito is None:
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar el documento de postulación"
        )

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    return {
        "mensaje": "Registro eliminado correctamente"
    }
