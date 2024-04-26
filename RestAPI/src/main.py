from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import dbInit
from Name.routes import route as NameRoute


TOKEN = "token"
client = None


app = FastAPI(title="DEEPHACK.AGENTS", lifespan=dbInit)


app.include_router(router=NameRoute)


origins = [
    "*",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
