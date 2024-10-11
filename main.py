from fastapi import FastAPI, Depends
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from database import engine, BaseSQL, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from schemas.schema_User import schema_User
from sqlalchemy.orm import Session
from models.models import model_User
from uuid import uuid4

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

# Dépendance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    BaseSQL.metadata.create_all(bind=engine)

@app.get('/')
async def get_root():
    return {'message':datetime.now().strftime('%d/%m/%Y')}

@app.post('/auth/inscription')
# Inscrition utilisateur
async def inscription(pUtilisateur: schema_User, pConfirmerMDP: str, db: Session = Depends(get_db)):
    if pUtilisateur.mot_de_passe == pConfirmerMDP:
        db_item = model_User(id=uuid4(), 
                             prenom=pUtilisateur.prenom, 
                             nom=pUtilisateur.nom, 
                             surnom=pUtilisateur.surnom,
                             email=pUtilisateur.email,
                             adresse_numero=pUtilisateur.adresse_numero,
                             adresse_rue=pUtilisateur.adresse_rue,
                             adresse_ville=pUtilisateur.adresse_ville,
                             mot_de_passe=pUtilisateur.mot_de_passe)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return {'message': 'Inscription réussie'}
    return {'message': 'Les mots de passe ne correspondent pas'}


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