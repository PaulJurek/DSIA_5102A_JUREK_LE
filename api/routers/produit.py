from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
import models
from services import produit as produit_service

router = APIRouter(prefix="/produits")

# Configuration de Jinja2Templates
templates = Jinja2Templates(directory="../api/templates")

@router.get("/", tags=["produits"])
async def get_produits(request: Request, db: Session = Depends(models.get_db), skip: int = 0, limit: int = 10):
    # Récupérer la liste des produits depuis la base de données avec pagination
    produits = produit_service.get_liste_produits(db=db, skip=skip, limit=limit)
    
    # Passer les produits et les paramètres de pagination au template
    return templates.TemplateResponse("index.html", {"request": request, "produits": produits, "skip": skip, "limit": limit})

# Route pour afficher la page de création de produit
@router.get("/ajouter", tags=["produits"])
async def ajouter_produit(request: Request):
    return templates.TemplateResponse("ajouter_produit.html", {"request": request})

# Route pour traiter la soumission du formulaire et ajouter le produit
@router.post("/ajouter", tags=["produits"])
async def ajouter_produit_post(nom: str = Form(...), description: str = Form(...), prix: float = Form(...), imageurl: str = Form(...), db: Session = Depends(models.get_db)):
    return produit_service.post_produit(nom=nom,description=description,prix=prix,imageurl=imageurl,db=db)

# Page pour sélectionner un produit à modifier
@router.get("/modifier", tags=["produits"])
async def modifier_produit_selection(request: Request, db: Session = Depends(models.get_db)):
    produits = produit_service.get_liste_produits(db=db, limit=100)  # Afficher jusqu'à 100 produits
    return templates.TemplateResponse("modifier_produit.html", {"request": request, "produits": produits})

# Formulaire de modification d'un produit spécifique
@router.get("/modifier/{produit_id}", tags=["produits"])
async def modifier_produit_form(request: Request, produit_id: str, db: Session = Depends(models.get_db)):
    produit = produit_service.get_produit_by_id(produit_id, db)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return templates.TemplateResponse("modifier_form.html", {"request": request, "produit": produit})

# Supprimer un produit spécifique
@router.post("/supprimer/{produit_id}", tags=["produits"])
async def supprimer_produit(produit_id: str, db: Session = Depends(models.get_db)):
    produit_service.delete_produit(produit_id, db)
    return RedirectResponse(url="/produits", status_code=303)