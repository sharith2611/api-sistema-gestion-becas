
from fastapi import APIRouter, HTTPException

from app.models.modulo_rol import ModuloRol
from app.repositories.modulo_rol_repo import ModuloRolRepository


router = APIRouter(
    prefix="/modulo-rol",
    tags=["Gestión Módulo-Rol"]
)

repo = ModuloRolRepository()


@router.get("/")
def listar_modulo_rol():
    registros = repo.obtener_todos()

    if registros is None:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar las relaciones módulo-rol"
        )

    return registros


@router.get("/{id_rol}")
def obtener_modulos_por_rol(id_rol: int):

    registros = repo.obtener_por_rol(id_rol)

    if registros is None:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar los módulos del rol"
        )

    return registros


@router.get("/{modulo_rol_id}")
def obtener_modulo_rol(modulo_rol_id: int):

    registro = repo.obtener_por_id(modulo_rol_id)

    if registro is None:
        raise HTTPException(
            status_code=404,
            detail="Relación módulo-rol no encontrada"
        )

    return registro


@router.post("/")
def crear_modulo_rol(modulo_rol: ModuloRol):

    nuevo_id = repo.crear(modulo_rol)

    if nuevo_id is None:
        raise HTTPException(
            status_code=400,
            detail="No fue posible registrar la relación módulo-rol. Verifica que el rol y el módulo existan y que la relación no esté duplicada."
        )

    return {
        "mensaje": "Relación módulo-rol registrada exitosamente",
        "id": nuevo_id
    }


@router.delete("/{modulo_rol_id}")
def eliminar_modulo_rol(modulo_rol_id: int):

    exito = repo.eliminar(modulo_rol_id)

    if exito is None:
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar la relación módulo-rol"
        )

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Relación módulo-rol no encontrada"
        )

    return {
        "mensaje": "Relación módulo-rol eliminada correctamente"
    }


@router.put("/{modulo_rol_id}")
def actualizar_modulo_rol(
    modulo_rol_id: int,
    modulo_rol: ModuloRol
):

    exito = repo.actualizar(
        modulo_rol_id,
        modulo_rol
    )

    if exito is None:
        raise HTTPException(
            status_code=400,
            detail="No fue posible actualizar la relación módulo-rol"
        )

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Relación módulo-rol no encontrada"
        )

    return {
        "mensaje": "Relación módulo-rol actualizada correctamente"
    }
