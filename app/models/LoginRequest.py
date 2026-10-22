from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    codigo_usuario: str
    clave: str