from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.users import user
from config import config

app = FastAPI()

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


@app.get("/")
async def read_root():
    return {"message": "Server running"}