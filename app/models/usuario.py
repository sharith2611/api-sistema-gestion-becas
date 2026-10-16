from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    codigo_usuario: str
    nombre: str
    cedula: str
    id_rol: int
    estado: bool = True
    clave: str
