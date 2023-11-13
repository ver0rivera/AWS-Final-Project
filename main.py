from fastapi import FastAPI, HTTPException, Path, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def standard_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
    
app.add_exception_handler(RequestValidationError,standard_validation_exception_handler)

class Alumno(BaseModel):
    id: Optional[int] = Field(default=None, example=1)
    nombres: str = Field(..., example="Juan")
    apellidos: str = Field(..., example="Pérez")
    matricula: str = Field(..., example="A01234567")
    promedio: float = Field(..., ge=0, le=100, example=95.5)  


class Profesor(BaseModel):
    id: Optional[int] = Field(default=None, example=1)
    numeroEmpleado: int = Field(..., example="P012345")
    nombres: str = Field(..., example="Laura")
    apellidos: str = Field(..., example="González")
    horasClase: int = Field(..., ge=0, example=10)  


alumnos = []
profesores = []

@app.get("/alumnos", response_model=List[Alumno])
def get_alumnos():
    return alumnos

@app.get("/alumnos/{alumno_id}", response_model=Alumno)
def get_alumno(alumno_id: int = Path(..., description="El ID del alumno a recuperar")):
    alumno = next((alumno for alumno in alumnos if alumno["id"] == alumno_id), None)
    if alumno is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alumno no encontrado")
    return alumno

@app.post("/alumnos", response_model=Alumno, status_code=status.HTTP_201_CREATED)
def create_alumno(alumno: Alumno):
    alumnos.append(alumno.dict())
    return alumno

@app.put("/alumnos/{alumno_id}", response_model=Alumno)
def update_alumno(alumno_id: int, alumno: Alumno):
    index = next((i for i, a in enumerate(alumnos) if a["id"] == alumno_id), None)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alumno no encontrado")
    alumno.id = alumno_id  
    alumnos[index] = alumno.dict()
    return alumno

@app.delete("/alumnos/{alumno_id}", response_model=Alumno)
def delete_alumno(alumno_id: int):
    index = next((i for i, a in enumerate(alumnos) if a["id"] == alumno_id), None)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alumno no encontrado")
    return alumnos.pop(index)


@app.get("/profesores", response_model=List[Profesor])
def get_profesores():
    return profesores

@app.get("/profesores/{profesor_id}", response_model=Profesor)
def get_profesor(profesor_id: int = Path(..., description="El ID del profesor a recuperar")):
    profesor = next((profesor for profesor in profesores if profesor["id"] == profesor_id), None)
    if profesor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
    return profesor

@app.post("/profesores", response_model=Profesor, status_code=status.HTTP_201_CREATED)
def create_profesor(profesor: Profesor):
    #profesor.id = len(profesores) + 1
    profesores.append(profesor.dict())
    return profesor

@app.put("/profesores/{profesor_id}", response_model=Profesor)
def update_profesor(profesor_id: int, profesor: Profesor):
    index = next((i for i, p in enumerate(profesores) if p["id"] == profesor_id), None)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
    profesor.id = profesor_id 
    profesores[index] = profesor.dict()
    return profesor

@app.delete("/profesores/{profesor_id}", response_model=Profesor)
def delete_profesor(profesor_id: int):
    index = next((i for i, p in enumerate(profesores) if p["id"] == profesor_id), None)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
    return profesores.pop(index)



