from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from starlette.requests import Request

from ..models.database import get_db
from ..schemas.posts import Post as schema_post
from ..services import posts as posts_service
from ..services.users import get_user_id
from utils import verify_autorization_header

post_router = APIRouter(prefix="/posts")

security = HTTPBearer()


@post_router.post("/", dependencies=[Depends(security)], tags=["posts"])
async def create_post(post: schema_post, user_id : str = Depends(get_user_id), db: Session = Depends(get_db)):
    return posts_service.create_post(user_id=user_id, post=post, db=db)


@post_router.get("/users", dependencies=[Depends(security)], tags=["posts_per_user"])
async def get_user_posts(
    token : int  = Depends(verify_autorization_header),
    db: Session = Depends(get_db),
) -> List[schema_post]:

    user_id = token.get("user_id")

    return posts_service.get_posts_for_user(db=db, user_id=user_id)


@post_router.get("/{post_id}", dependencies=[Depends(security)], tags=["posts"])
async def get_post_by_id(
    post_id: str, request: Request, token: int = Depends(verify_autorization_header), db: Session = Depends(get_db)
):
    auth_header = request.headers.get("Authorization")

    token = verify_autorization_header(auth_header)

    post = posts_service.get_post_by_id(post_id=post_id, db=db)

    if str(post.user_id) != token.get("user_id"):
        raise HTTPException(
            status_code=403, detail=f"Forbidden {post.user_id} {token.get('user_id')}"
        )

    return post


@post_router.get("/", tags=["posts"])
async def get_posts(db: Session = Depends(get_db)):
    return posts_service.get_all_posts(db=db)


@post_router.put("/{post_id}", dependencies=[Depends(security)], tags=["posts"])
async def update_post_by_id(
    post_id: str, post: schema_post, db: Session = Depends(get_db)
):
    return posts_service.update_post(post_id=post_id, db=db, post=post)


@post_router.delete("/{post_id}", tags=["posts"])
async def delete_post_by_id(post_id: str, db: Session = Depends(get_db)):
    return posts_service.delete_post(post_id=post_id, db=db)


@post_router.delete("/", tags=["posts"])
async def delete_all_posts(db: Session = Depends(get_db)):
    return posts_service.delete_all_posts(db=db)
