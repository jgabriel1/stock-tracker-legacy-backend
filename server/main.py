from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import routes
from .settings.allowed_hosts import PWA_URL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[PWA_URL],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)

app.include_router(routes.router)
