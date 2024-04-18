from fastapi import FastAPI
from Name.routes import route as NameRoute


TOKEN = "token"

app = FastAPI(title="DEEPHACK.AGENTS")

app.include_router(router=NameRoute)
