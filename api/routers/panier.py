from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from jose.exceptions import JWTError
from models import get_db
from services import auth as auth_service
from services import utilisateur as utilisateur_service
from services import panier as panier_service
from services import produit as produit_service
from schemas import schema_Panier

router = APIRouter(prefix="/panier")

# Configuration de Jinja2Templates
templates = Jinja2Templates(directory="../api/templates")

@router.get("/", tags=["panier"])
async def get_paniers(request: Request, db: Session = Depends(get_db)):
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
    
    paniers, grand_total = panier_service.get_liste_paniers_utilisateur(db=db, nom_utilisateur=utilisateur.nom_utilisateur)
    return templates.TemplateResponse("liste_paniers.html", {"request": request, "paniers": paniers, "grand_total": grand_total})

@router.post("/supprimer/{panier_id}", tags=["panier"])
async def supprimer_panier(request: Request, panier_id: str, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        return RedirectResponse(url="/auth/connexion", status_code=303)
    try:
        nom_utilisateur = await auth_service.get_nom_utilisateur(token)
    except JWTError:
        pass
    utilisateur = utilisateur_service.get_utilisateur_par_nom(db=db, nom_utilisateur=nom_utilisateur)
    panier = panier_service.get_panier_by_id(db=db,panier_id=panier_id)
    if not panier:
        raise HTTPException(status_code=404, detail="Panier non trouvé")
    if utilisateur.nom_utilisateur != panier.nom_utilisateur:
        raise HTTPException(status_code=40, detail="Action non autorisée")
    panier_service.delete_panier(db=db,panier_id=panier_id)
    return RedirectResponse(url="/panier", status_code=303)

@router.post("/ajouter/{produit_id}", tags=["produits"])
async def ajouter_produit_post(request: Request, produit_id: str, quantite: int = Form(...), db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        return RedirectResponse(url="/auth/connexion", status_code=303)
    try:
        nom_utilisateur = await auth_service.get_nom_utilisateur(token)
    except JWTError:
        pass
    produit = produit_service.get_produit_by_id(db=db,produit_id=produit_id)
    panier = schema_Panier(
        nom_produit= produit.nom,
        nom_utilisateur = nom_utilisateur,
        quantite = quantite,
        prix_total = produit.prix
    )
    panier_service.post_produit_panier(panier=panier,db=db)
    return RedirectResponse(url="/produits", status_code=303)


@router.get("/commander", tags=["produits"])
async def commander(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        return RedirectResponse(url="/auth/connexion", status_code=303)
    try:
        nom_utilisateur = await auth_service.get_nom_utilisateur(token)
    except JWTError:
        pass
    panier_service.commander(db=db, nom_utilisateur=nom_utilisateur)
    return RedirectResponse(url="/commandes", status_code=303)