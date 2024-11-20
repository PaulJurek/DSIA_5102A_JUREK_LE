# routers/commande.py
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
import models
from services import commande as commande_service
from typing import List

router = APIRouter(prefix="/commandes")

# Configuration de Jinja2Templates
templates = Jinja2Templates(directory="../api/templates")

# Route pour afficher toutes les commandes
@router.get("/", tags=["commandes"])
async def get_commandes(request: Request, db: Session = Depends(models.get_db), skip: int = 0, limit: int = 10):
    # Récupérer la liste des commandes depuis la base de données avec pagination
    commandes = commande_service.get_liste_commandes(db=db, skip=skip, limit=limit)
    
    # Passer les commandes et les paramètres de pagination au template
    return templates.TemplateResponse("commandes.html", {"request": request, "commandes": commandes, "skip": skip, "limit": limit})

# Route pour afficher une page de détail d'une commande
@router.get("/{commande_id}", tags=["commandes"])
async def get_commande_detail(request: Request, commande_id: str, db: Session = Depends(models.get_db)):
    commande = commande_service.get_commande_by_id(commande_id, db)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    
    return templates.TemplateResponse("commande_detail.html", {"request": request, "commande": commande})

# Route pour créer une nouvelle commande
@router.get("/ajouter", tags=["commandes"])
async def ajouter_commande(request: Request):
    return templates.TemplateResponse("ajouter_commande.html", {"request": request})

# Route pour ajouter une commande
@router.post("/ajouter", tags=["commandes"])
async def ajouter_commande_post(db: Session = Depends(models.get_db), produits_ids: List[str] = Form(...)):
    return commande_service.post_commande(produits_ids=produits_ids, db=db)

# Route pour supprimer une commande spécifique
@router.post("/supprimer/{commande_id}", tags=["commandes"])
async def supprimer_commande(commande_id: str, db: Session = Depends(models.get_db)):
    commande_service.delete_commande(commande_id, db)
    return RedirectResponse(url="/commandes", status_code=303)
