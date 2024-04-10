from fastapi import FastAPI

from backend_python.app.api import router

app = FastAPI()

app.include_router(router)
