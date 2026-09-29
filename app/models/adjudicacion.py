from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Adjudicacion(BaseModel):
    id_adjudicacion: Optional[int] = None
    id_postulacion: int
    fecha_adjudicacion: datetime
    resultado: str
    porcentaje_aprobado: float
    monto_aprobado:float 
    observaciones: Optional[str] = None
    estado: Optional[bool] = True 