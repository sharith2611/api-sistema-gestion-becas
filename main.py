from fastapi import FastAPI
from app.api import (
    rutas_adjudicacion,
    rutas_auxilio_educativo,
    rutas_convocatoria,
    rutas_documento_adjudicacion,
    rutas_estudiante,
    rutas_facultad,
    rutas_institucion,
    rutas_postulacion,
    rutas_usuario,
    rutas_modulo,
    rutas_modulo_rol,
    rutas_programa_academico,
    rutas_requisito_convocatoria,
  
)

app = FastAPI(
    title="API Sistema de auxilio Educativo",
    description="Backend modular con FastAPI y PostgreSQL (Neon) para Sistema Auxilio Educativo",
    version="1.0.0"
)

# Conectamos cada modulo de rutas a la aplicacion principal
app.include_router(rutas_adjudicacion.router)
app.include_router(rutas_auxilio_educativo.router)
app.include_router(rutas_convocatoria.router)
app.include_router(rutas_documento_adjudicacion.router)
app.include_router(rutas_estudiante.router)
app.include_router(rutas_facultad.router)
app.include_router(rutas_postulacion.router)
app.include_router(rutas_usuario.router)
app.include_router(rutas_modulo.router)
app.include_router(rutas_modulo_rol.router)
app.include_router(rutas_institucion.router)
app.include_router(rutas_programa_academico.router)
app.include_router(rutas_requisito_convocatoria.router)



@app.get("/")
def estado_api():
    return {"mensaje": "API Para Sistema de auxilios Educativos"}
