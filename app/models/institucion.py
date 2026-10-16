from pydantic import BaseModel
from typing import Optional


class Institucion(BaseModel):
    nombre: str
    direccion: str
    telefono: str
    email: str
    estado: bool = True