from pydantic import BaseModel
from typing import Optional
from datetime import date




class ProgramaAcademico(BaseModel):
    id_programa: Optional[int] = None
    id_facultad: int
    codigo: str
    nombre: str
    nivel: str
    modalidad: str
    estado: bool = True
    estado: Optional[bool] = True 