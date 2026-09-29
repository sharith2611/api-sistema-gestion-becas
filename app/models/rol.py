
from pydantic import BaseModel
from typing import Optional
from datetime import date


class Rol(BaseModel):
    id_rol: Optional[int] = None
    descripcion: str
    estado : Optional[bool] =True
    


