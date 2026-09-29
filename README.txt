entorno:
pip install virtualenv


lista:
Pip list


Crear entorno:
python -m venv myvenv


Activar entorno:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
cd myvenv 
cd .\Scripts\ 
.\activate


Aplicar dos veces:
cd..

Instalar dependencias permitidas:
pip install fastapi uvicorn psycopg2-binary pydantic pydantic-settings

Para correrlo:
uvicorn main:app --reload