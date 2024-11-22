from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models.database import get_db
from ..schemas.users import User, User_infos_de_connexion
from ..services.users import create_user
from ..services.auth import generate_access_token


user_router = APIRouter(prefix="/users")

@user_router.post("/", tags=["users"])
async def post_user(user: User, db: Session = Depends(get_db)):
    return create_user(user=user, db=db)

@user_router.post('/auth/connexion')
# Connexion utilisateur,commercant
async def connexion(user_login: User_infos_de_connexion):
    access_token = generate_access_token(db=get_db, user_login=user_login)
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get('/consultation/{id}', tag=["users"])
# consultations données utilisateur
async def consultation():
    pass

@user_router.post('/auth/inscription', tag=["users"])
# Inscrition utilisateur
async def inscription(pConfirmerMDP: str, pUtilisateur: User,db: Session = Depends(get_db) ):
    create_user(db=db, user=pUtilisateur, pConfirmerMDP=pConfirmerMDP)


@user_router.delete('/desinscription/', tag=["users"])
# Desinscription utilisateur
async def desinscription(user :User, db: Session = Depends(get_db)):
    if user in db:
        del db[user]
        return {"message": "Utilisateur supprimé avec succès."}
    else:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable.")
    
@user_router.put('/modification/', tags=["users"])
# modification données utilisateur
async def modification(user :User, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe
    utilisateur_data = db.get(user.pseudo)
    if not utilisateur_data:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable.")
    
    # Mise à jour du prenom si fourni
    if user.prenom:
        utilisateur_data["prenom"] = user.prenom
    
    # Mise à jour du nom si fourni
    if user.nom:
        utilisateur_data["nom"] = user.nom
    
    # Mise à jour du pseudo si fourni
    if user.pseudo:
        utilisateur_data["pseudo"] = user.pseudo
    
    # Mise à jour du mail si fourni
    if user.email:
        utilisateur_data["email"] = user.email

    # Mise à jour de l'adresse de résidence si fournie
    if user.adresse_numero:
        utilisateur_data["adresse_numero"] = user.adresse_numero
    if user.adresse_rue:
        utilisateur_data["adresse_rue"] = user.adresse_rue
    if user.adresse_ville:
        utilisateur_data["adresse_numero"] = user.adresse_ville
    
    #Mise à jour du mot de passe si fourni
    if user.mot_de_passe:
        utilisateur_data["mot_de_passe"] = user.mot_de_passe
    
    return {"message": "Coordonnées mises à jour avec succès.", "utilisateur": utilisateur_data}