import sqlmodel
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select
from fastapi import FastAPI, HTTPException
#vamos a crear una tabla, en este caso en python se le llama clase así que colocaremos class
class Paralelo(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    nombre:str
    aula:str
class Materia(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    nombre:str
    codigo:str
    creditos:int
class Usuario(SQLModel, table=True):
    id: Optional[int]=Field(default=None, primary_key=True)
    nombres: str
    apellidos: str
    correo: str
    paralelo_id: Optional[int] = Field(default=None, foreign_key="paralelo.id")

#python creará un archivo con el nombre que le indiquemos ahora
DATABASE_URL = "sqlite:///./escuela.db"
#el motor que se comunicará con sqlite
engine = create_engine(DATABASE_URL, echo=False)
#vamos con el fastapi
app = FastAPI(
    title="Sistema de organización de la Uni",
    description="API CRUD para Usuarios, Materias y Paralelos",
    version="1.0"
)
@app.on_event("startup")
def inicio():
    SQLModel.metadata.create_all(engine)

#AHORA SI VAMOS CON EL CRUDDDDD   

# 1. READ ALL: Listar todos los estudiantes
@app.get("/usuarios/", tags=["Usuarios"])
def obtener_usuarios():
    with Session(engine) as session:
        usuarios = session.exec(select(Usuario)).all()
        return usuarios

# 2. READ ONE: Obtener un estudiante por ID
@app.get("/usuarios/{usuario_id}", tags=["Usuarios"])
def obtener_usuario(usuario_id: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario

# 3. CREATE: Agregar un nuevo usuario
@app.post("/usuarios/", tags=["Usuarios"])
def crear_usuario(usuario: Usuario):
    with Session(engine) as session:
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario

# 4. UPDATE: Modificar datos de un usuario existente
@app.put("/usuarios/{usuario_id}", tags=["Usuarios"])
def actualizar_usuario(usuario_id: int, datos_nuevos: Usuario):
    with Session(engine) as session:
        usuario_db = session.get(Usuario, usuario_id)
        if not usuario_db:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        usuario_db.nombres = datos_nuevos.nombres
        usuario_db.apellidos = datos_nuevos.apellidos
        usuario_db.correo = datos_nuevos.correo
        usuario_db.paralelo_id = datos_nuevos.paralelo_id

        session.add(usuario_db)
        session.commit()
        session.refresh(usuario_db)
        return usuario_db

# 5. DELETE: Eliminar un usuario
@app.delete("/usuarios/{usuario_id}", tags=["Usuarios"])
def eliminar_usuario(usuario_id: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        session.delete(usuario)
        session.commit()
        return {"mensaje": f"Usuario con ID {usuario_id} eliminado exitosamente"}


@app.get("/paralelos/", tags=["Paralelos"])
def obtener_paralelos():
    with Session(engine) as session:
        return session.exec(select(Paralelo)).all()

@app.post("/paralelos/", tags=["Paralelos"])
def crear_paralelo(paralelo: Paralelo):
    with Session(engine) as session:
        session.add(paralelo)
        session.commit()
        session.refresh(paralelo)
        return paralelo

@app.delete("/paralelos/{paralelo_id}", tags=["Paralelos"])
def eliminar_paralelo(paralelo_id: int):
    with Session(engine) as session:
        paralelo = session.get(Paralelo, paralelo_id)
        if not paralelo:
            raise HTTPException(status_code=404, detail="Paralelo no encontrado")
        session.delete(paralelo)
        session.commit()
        return {"mensaje": "Paralelo eliminado"}


@app.get("/materias/", tags=["Materias"])
def obtener_materias():
    with Session(engine) as session:
        return session.exec(select(Materia)).all()

@app.post("/materias/", tags=["Materias"])
def crear_materia(materia: Materia):
    with Session(engine) as session:
        session.add(materia)
        session.commit()
        session.refresh(materia)
        return materia

@app.delete("/materias/{materia_id}", tags=["Materias"])
def eliminar_materia(materia_id: int):
    with Session(engine) as session:
        materia = session.get(Materia, materia_id)
        if not materia:
            raise HTTPException(status_code=404, detail="Materia no encontrada")
        session.delete(materia)
        session.commit()
        return {"mensaje": "Materia eliminada"}