from pydantic import BaseModel
from typing import Optional
from datetime import date




class Convocatoria(BaseModel):
    id_convocatoria: Optional[int] = None
    id_auxilio : int
    nombre: str
    fecha_inicio: date
    fecha_fin: date
    cupos: int 
    estado: Optional[bool] = True
    