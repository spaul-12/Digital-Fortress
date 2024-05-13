from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.auth import auth
from config import config
from contextlib import asynccontextmanager
from services.utils import init_db,db_close

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    """
    await init_db()
    yield
    await db_close()



app = FastAPI(lifespan=lifespan)

origins = [
    config.get("CORS_ORIGIN"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/")
async def read_root():
    return {"message": "Server running"}