from pydantic import BaseModel
from typing import Optional


class ModuloRol(BaseModel):
    id_modulo_rol: Optional[int] = None
    id_rol: int
    id_modulo: int
    estado: bool = True
  