
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentoAdjudicacion(BaseModel):
    id_documento_adjudicacion: Optional[int] = None
    id_adjudicacion: int
    nombre_archivo: str
    ruta_archivo: str
    fecha_carga: datetime
    estado: Optional[bool] = True
    observacion: Optional[str] = None
   