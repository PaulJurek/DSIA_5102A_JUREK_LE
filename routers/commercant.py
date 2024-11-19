from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.database import get_db
from schemas.commercant import Commercant
from services.commercant import create_commercant, lister_tous_utilisateurs

user_router = APIRouter(prefix="/commercant")


@user_router.post("/", tags=["commercant"])
async def post_commercant(commercant: Commercant, db: Session = Depends(get_db)):
    return create_commercant(user=commercant, db=db)


@user_router.get("/", tags=["commercant"])
async def recuperer_tous_utilisateurs(db: Session = Depends(get_db)) -> List[Commercant]:
    return lister_tous_utilisateurs(db=db)

@user_router.get('/consultation/{id}')
# consultations données utilisateur
async def consultation():
    pass

@user_router.delete('/desinscription/', tag=["commercant"])
# Desinscription utilisateur
async def desinscription(commercant : Commercant, db: Session = Depends(get_db)):
    if commercant in db:
        del db[commercant]
        return {"message": "Utilisateur supprimé avec succès."}
    else:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable.")
    
@user_router.put('/modification/', tags=["commercant"])
# modification données utilisateur
async def modification(commercant : Commercant, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe
    utilisateur_data = db.get(commercant.pseudo)
    if not utilisateur_data:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable.")
    
    # Mise à jour du prenom si fourni
    if commercant.prenom:
        utilisateur_data["prenom"] = commercant.prenom
    
    # Mise à jour du nom si fourni
    if commercant.nom:
        utilisateur_data["nom"] = commercant.nom
    
    # Mise à jour du pseudo si fourni
    if commercant.pseudo:
        utilisateur_data["pseudo"] = commercant.pseudo
    
    # Mise à jour du mail si fourni
    if commercant.email:
        utilisateur_data["email"] = commercant.email

    # Mise à jour de l'adresse de résidence si fournie
    if commercant.adresse_numero:
        utilisateur_data["adresse_numero"] = commercant.adresse_numero
    if commercant.adresse_rue:
        utilisateur_data["adresse_rue"] = commercant.adresse_rue
    if commercant.adresse_ville:
        utilisateur_data["adresse_numero"] = commercant.adresse_ville
    
    #Mise à jour du mot de passe si fourni
    if commercant.mot_de_passe:
        utilisateur_data["mot_de_passe"] = commercant.mot_de_passe
    
    return {"message": "Coordonnées mises à jour avec succès.", "utilisateur": utilisateur_data}