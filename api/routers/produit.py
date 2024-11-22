from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from jose.exceptions import JWTError
from models import get_db
from schemas import schema_Produit
from services import produit as produit_service
from services import auth as auth_service
from services import utilisateur as utilisateur_service

router = APIRouter(prefix="/produits")

# Configuration de Jinja2Templates
templates = Jinja2Templates(directory="../api/templates")

@router.get("/", tags=["produits"])
async def get_produits(request: Request, db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        return RedirectResponse(url="/auth/connexion", status_code=303)
    try:
        nom_utilisateur = await auth_service.get_nom_utilisateur(token)
    except JWTError:
        pass

    # Récupération de l'utilisateur
    utilisateur = utilisateur_service.get_utilisateur_par_nom(db=db, nom_utilisateur=nom_utilisateur)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Récupérer la liste des produits depuis la base de données avec pagination
    produits = produit_service.get_liste_produits(db=db, skip=skip, limit=limit)

    # Passer les produits et les paramètres de pagination au template
    return templates.TemplateResponse("liste_produits.html", {"request": request, "nom_utilisateur": nom_utilisateur, "produits": produits, "skip": skip, "limit": limit})


@router.get("/ajouter", tags=["produits"])
async def ajouter_produit(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        return RedirectResponse(url="/auth/connexion", status_code=303)
    try:
        nom_utilisateur = await auth_service.get_nom_utilisateur(token)
    except JWTError:
        pass
    utilisateur = utilisateur_service.get_utilisateur_par_nom(db=db, nom_utilisateur=nom_utilisateur)
    if not utilisateur_service.utilisateur_est_admin(db=db,nom_utilisateur=nom_utilisateur):
        raise HTTPException(status_code=403, detail="Accès refusé")
    return templates.TemplateResponse("ajouter_produit.html", {"request": request})

# Route pour traiter la soumission du formulaire et ajouter le produit
@router.post("/ajouter", tags=["produits"])
async def ajouter_produit_post(request: Request, nom: str = Form(...), description: str = Form(...), prix: float = Form(...), imageurl: str = Form(...), db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        return RedirectResponse(url="/auth/connexion", status_code=303)
    try:
        nom_utilisateur = await auth_service.get_nom_utilisateur(token)
    except JWTError:
        pass
    if not utilisateur_service.utilisateur_est_admin(db=db,nom_utilisateur=nom_utilisateur):
        raise HTTPException(status_code=403, detail="Accès refusé")
    produit = schema_Produit(
        nom = nom,
        description = description,
        prix = prix,
        imageurl = imageurl
    )
    produit_service.post_produit(produit=produit,db=db)
    return RedirectResponse(url="/produits", status_code=303)

# Formulaire de modification d'un produit spécifique
@router.get("/modifier/{produit_id}", tags=["produits"])
async def modifier_produit_form(request: Request, produit_id: str, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        return RedirectResponse(url="/auth/connexion", status_code=303)
    try:
        nom_utilisateur = await auth_service.get_nom_utilisateur(token)
    except JWTError:
        pass
    utilisateur = utilisateur_service.get_utilisateur_par_nom(db=db, nom_utilisateur=nom_utilisateur)
    if not utilisateur_service.utilisateur_est_admin(db=db,nom_utilisateur=nom_utilisateur):
        raise HTTPException(status_code=403, detail="Accès refusé")
    produit = produit_service.get_produit_by_id(produit_id, db)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return templates.TemplateResponse("modifier_produit.html", {"request": request, "produit": produit})

# Traitement des modifications
@router.post("/modifier/{produit_id}", tags=["produits"])
async def modifier_produit(request: Request, produit_id: str, nom: str = Form(...), description: str = Form(None), prix: float = Form(...), imageurl: str = Form(None), db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        return RedirectResponse(url="/auth/connexion", status_code=303)
    try:
        nom_utilisateur = await auth_service.get_nom_utilisateur(token)
    except JWTError:
        pass
    if not utilisateur_service.utilisateur_est_admin(db=db,nom_utilisateur=nom_utilisateur):
        raise HTTPException(status_code=403, detail="Accès refusé")
    produit = schema_Produit(
        id = produit_id,
        nom = nom,
        description = description,
        prix = prix,
        imageurl = imageurl
    )
    produit_service.update_produit(produit, db)
    return RedirectResponse(url="/produits", status_code=303)

# Formulaire de modification d'un produit spécifique
@router.get("/supprimer/{produit_id}", tags=["produits"])
async def supprimer_produit_form(request: Request, produit_id: str, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        return RedirectResponse(url="/auth/connexion", status_code=303)
    try:
        nom_utilisateur = await auth_service.get_nom_utilisateur(token)
    except JWTError:
        pass
    utilisateur = utilisateur_service.get_utilisateur_par_nom(db=db, nom_utilisateur=nom_utilisateur)
    if not utilisateur_service.utilisateur_est_admin(db=db,nom_utilisateur=nom_utilisateur):
        raise HTTPException(status_code=403, detail="Accès refusé")   
    produit = produit_service.get_produit_by_id(produit_id, db)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return templates.TemplateResponse("supprimer_produit.html", {"request": request, "produit": produit})

# Supprimer un produit spécifique
@router.post("/supprimer/{produit_id}", tags=["produits"])
async def supprimer_produit(request: Request, produit_id: str, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        return RedirectResponse(url="/auth/connexion", status_code=303)
    try:
        nom_utilisateur = await auth_service.get_nom_utilisateur(token)
    except JWTError:
        pass
    if not utilisateur_service.utilisateur_est_admin(db=db,nom_utilisateur=nom_utilisateur):
        raise HTTPException(status_code=403, detail="Accès refusé")  
    produit_service.delete_produit(produit_id, db)
    return RedirectResponse(url="/produits", status_code=303)
