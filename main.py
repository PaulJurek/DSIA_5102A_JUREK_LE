from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.dialects.postgresql import UUID

from models.database import engine, BaseSQL, get_db
from schemas.users import User
from sqlalchemy.orm import Session
from models.user import User
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

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    BaseSQL.metadata.create_all(bind=engine)

@app.get('/', response_class=HTMLResponse)
async def root(request:Request):
    return templates.TemplateResponse("accueil.html", {"request": request})

@app.post('/auth/inscription')
# Inscrition utilisateur
async def inscription(pUtilisateur: User, pConfirmerMDP: str, db: Session = Depends(get_db)):
    if pUtilisateur.mot_de_passe == pConfirmerMDP:
        db_item = User(id=uuid4(), 
                             prenom=pUtilisateur.prenom, 
                             nom=pUtilisateur.nom, 
                             pseudo=pUtilisateur.pseudo,
                             email=pUtilisateur.email,
                             date_naissance=pUtilisateur.date_naissance,
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
# Connexion utilisateur,commercant
async def connexion():
    pass
