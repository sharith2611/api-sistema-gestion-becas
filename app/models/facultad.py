from pydantic import BaseModel
from typing import Optional
from datetime import date


class Facultad (BaseModel):
    id_facultad: Optional[int] = None
    id_institucion: int
    nombre : str
    direccion: str
    Ext: str
    email: Optional[str] = None
    estado: bool = True
 
    
    
      
