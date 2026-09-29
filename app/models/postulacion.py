from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Postulacion(BaseModel):
    id_postulacion: Optional[int] = None
    id_estudiante: int
    id_convocatoria: int
    fecha_postulacion: datetime
    estado: str
    observaciones: Optional[str] = None
    adjuntos: Optional[str] = None
    estado: Optional[bool] = True 