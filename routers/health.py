from fastapi import FastAPI, Header, Request, APIRouter
from typing import Optional
import base64
import json

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Bienvenue sur le site de E-commerce !"}


@router.get("/health")
def read_root():
    return {"message": "Api fonctionne correctement !"}

"""
@router.get("/api/headers")
def read_hello(
    request: Request, x_userinfo: Optional[str] = Header(None, convert_underscores=True)
):
    print(request["headers"])
    return {"Headers": x_userinfo}
"""