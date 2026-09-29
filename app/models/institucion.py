from pydantic import BaseModel
from typing import Optional


class Institucion(BaseModel):
    id_institucion: Optional[int] = None
    nombre: str
    direccion: str
    telefono: str
    email: str
    estado: bool = True