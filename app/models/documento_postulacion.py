
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentoPostulacion(BaseModel):
    id_documento_postulacion: Optional[int] = None
    id_postulacion: int
    nombre_archivo: str
    ruta_archivo: Optional[str] = None
    fecha_carga: Optional[datetime] = None
    estado: bool = True
    observacion: Optional[str] = None
