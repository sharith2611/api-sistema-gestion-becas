from pydantic import BaseModel
from typing import Optional
from datetime import date

class auxilio_educativo (BaseModel):    
    id_auxilio: Optional[int] = None
    id_facultad: int
    nombre : str
    descripcion: str
    porcentaje_maximo: float
    monto_maximo: float 
    estado: Optional[bool] = True 
    tipo_auxilio: str
   