from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from jose.exceptions import JWTError
from models import get_db
from services import auth as auth_service
from services import utilisateur as utilisateur_service
from services import commande as commande_service
from services import panier as panier_service

router = APIRouter(prefix="/commandes")

# Configuration de Jinja2Templates
templates = Jinja2Templates(directory="../api/templates")

@router.get("/", tags=["commandes"])
async def get_commandes(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        return RedirectResponse(url="/auth/connexion", status_code=303)
    try:
        nom_utilisateur = await auth_service.get_nom_utilisateur(token)
    except JWTError:
        pass

    utilisateur = utilisateur_service.get_utilisateur_par_nom(db=db, nom_utilisateur=nom_utilisateur)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    commandes = commande_service.get_liste_commandes_utilisateur(db=db, nom_utilisateur=utilisateur.nom_utilisateur)
    return templates.TemplateResponse("liste_commandes.html", {"request": request, "commandes": commandes})

@router.get("/voircommandes", tags=["commandes"])
async def get_toutes_les_commandes(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        return RedirectResponse(url="/auth/connexion", status_code=303)
    try:
        nom_utilisateur = await auth_service.get_nom_utilisateur(token)
    except JWTError:
        pass
    if not utilisateur_service.utilisateur_est_admin(db=db,nom_utilisateur=nom_utilisateur):
        raise HTTPException(status_code=403, detail="Accès refusé") 
    commandes = commande_service.get_commandes(db=db)
    return templates.TemplateResponse("toutes_commandes.html", {"request": request, "commandes": commandes})

@router.post("/supprimer/{commande_id}", tags=["commandes"])
async def supprimer_commande(request: Request, commande_id: str, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        return RedirectResponse(url="/auth/connexion", status_code=303)
    try:
        nom_utilisateur = await auth_service.get_nom_utilisateur(token)
    except JWTError:
        pass
    if not utilisateur_service.utilisateur_est_admin(db=db,nom_utilisateur=nom_utilisateur):
        raise HTTPException(status_code=403, detail="Accès refusé") 
    panier = panier_service.get_panier_by_id(db=db,panier_id=commande_id)
    if not panier:
        raise HTTPException(status_code=404, detail="Panier non trouvé")
    panier_service.delete_panier(db=db,panier_id=commande_id)
    return RedirectResponse(url="/voircommandes", status_code=303)
