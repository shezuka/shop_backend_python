from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend_python.app.api import router

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
)

app.include_router(router, prefix="/api")
