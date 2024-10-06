from fastapi import FastAPI
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
#from models.models import BaseSQL
from database import engine, BaseSQL
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="My title",
    description="My description",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    BaseSQL.metadata.create_all(bind=engine)

@app.get('/')
async def get_root():
    return {'message':datetime.now().strftime('%d/%m/%Y')}

@app.post('/auth/inscription')
# Inscrition utilisateur
async def inscription():
    pass

@app.post('/auth/connexion')
# Connexion utilisateur
async def connexion():
    pass

# @app.delete('/user/desinscription/{id}')
# # Desinscription utilisateur
# async def desinscription(id: UUID):
#     pass

# @app.put('/user/modification/{id}')
# # modification données utilisateur
# async def modification(id: UUID):
#     pass

# @app.get('/user/consultation/{id}')
# # consultations données utilisateur
# async def consultation():
#     pass