from pydantic import BaseModel
from typing import Optional




class RequisitoConvocatoria(BaseModel):
    id_requisito_convocatoria: Optional[int] = None
    id_convocatoria: int
    descripcion: str
    obligatorio: bool = True
    valor_minimo: float
    estado: Optional[bool] = True 