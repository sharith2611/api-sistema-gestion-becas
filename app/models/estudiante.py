from pydantic import BaseModel
from typing import Optional
from datetime import date


class Estudiante(BaseModel):
    id_estudiante: Optional[int] = None
    id_programa: int
    documento: str
    nombres: str
    apellidos: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    fecha_ingreso: date
    estado: Optional[bool] = True 
    