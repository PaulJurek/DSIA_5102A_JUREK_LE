from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
from schemas.auth_token import AuthToken
from schemas.users import User
from services.auth import generate_access_token, get_user_id

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/token", tags=["auth"])
async def get_access_token(
    user_login: User,
    db: Session = Depends(models.get_db),
) -> AuthToken:
    access_token = generate_access_token(db=db, user_login=user_login)
    return AuthToken(
        access_token=access_token,
    )


@auth_router.get("/users/me")
async def read_users_me(token: str = Depends(AuthToken)):
    user = get_user_id()
    if user is None:
        raise HTTPException(status_code=401, detail="Votre compte a été supprimé ou vous ne l'avez pas encore créé")
    return user
