from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from models.database import engine, BaseSQL, get_db
import routers

app = FastAPI(
    title="Mon site de e-commerce",
    description="My description",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

app.include_router(routers.auth_router)
app.include_router(routers.user_router)
app.include_router(routers.post_router)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    BaseSQL.metadata.create_all(bind=engine)

@app.get('/', response_class=HTMLResponse)
async def root(request:Request):
    return templates.TemplateResponse("accueil.html", {"request": request})

