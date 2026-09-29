from pydantic import BaseModel
from typing import Optional


class ModuloRol(BaseModel):
    id_modulo_rol: Optional[int] = None
    id_modulo: int
    id_usuario: int
    estado: Optional[bool] = True 