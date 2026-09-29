from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    nombre: str
    cedula: str
    telefono: Optional[str] = None
    nivel: str
    estado: Optional[bool] = True 