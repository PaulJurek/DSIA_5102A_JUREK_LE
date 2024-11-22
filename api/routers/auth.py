from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from models import get_db
from schemas import schema_Utilisateur
from services import utilisateur as utilisateur_service
from services import auth as auth_service

router = APIRouter(prefix="/auth")

# Configuration de Jinja2Templates
templates = Jinja2Templates(directory="../api/templates")

@router.get("/inscription", tags=["auth"])
async def get_inscription(request: Request):
    return templates.TemplateResponse("inscription.html", {"request": request})

@router.post("/inscription", tags=["auth"])
async def post_inscription(db: Session = Depends(get_db), nom_utilisateur: str = Form(...), mot_de_passe: str = Form(...), confirmer: str = Form(...)):
    if mot_de_passe != confirmer:
        raise HTTPException(status_code=400, detail="Les mots de passe sont différents")
    
    utilisateur_inscription = schema_Utilisateur(
        nom_utilisateur = nom_utilisateur,
        mot_de_passe = mot_de_passe
    )
    utilisateur_service.post_utilisateur(db=db, utilisateur_inscription=utilisateur_inscription)
    return RedirectResponse(url="/auth/connexion", status_code=303)

@router.get("/connexion", tags=["auth"])
async def get_connexion(request: Request):
    return templates.TemplateResponse("connexion.html", {"request": request})

@router.post("/connexion", tags=["auth"])
async def post_connexion(db: Session = Depends(get_db), nom_utilisateur: str = Form(...), mot_de_passe: str = Form(...)):
    utilisateur_connexion = schema_Utilisateur(
        nom_utilisateur = nom_utilisateur,
        mot_de_passe = mot_de_passe
    )
    access_token = auth_service.connexion(db=db, utilisateur_connexion=utilisateur_connexion)
    response = RedirectResponse(url="/produits", status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=False, secure=False, max_age=3600) # Enregistrer le token JWT dans un cookie
    return response

@router.get("/deconnexion")
async def deconnexion(request: Request):
    response = RedirectResponse(url="/auth/connexion")
    response.delete_cookie("access_token") # Effacer le token JWT issu du cookie du navigateur
    return response

