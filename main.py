from email.mime import base
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastauth.auth import jwt_google

from fastauth.db import base
from fastauth.db.database import engine, sessionlocal
from fastapi.middleware.cors import CORSMiddleware
from fastauth.routers import user, item
from fastauth.auth.auth_google import auth_app
base.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.user_router)
app.include_router(item.item_router)

app.mount('/google', auth_app)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', tags=["GOOGLE LOGIN"])
def root():
    return HTMLResponse('<body><a href="/google/login">Log In</a></body>')


@app.get('/me', tags=["GOOGLE LOGIN"])
def get_my_user_name(token: str):
    # return {'token': token}
    return jwt_google.get_current_user_email(token)
