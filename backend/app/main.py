import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import sanity_sync
from .database import engine
from .models import Base
from .routes import admin, recommend
from .sanity_sync import start_scheduler

logger = logging.getLogger("stackx.main")


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    Base.metadata.create_all(bind=engine)
    if os.getenv('SANITY_PROJECT_ID'):
        try:
            sanity_sync.sync()
        except Exception as e:
            logger.error("Sanity sync failed on startup: %s", e)
        try:
            start_scheduler(sanity_sync.sync)
        except Exception as e:
            logger.error("Scheduler start failed: %s", e)
    yield


app = FastAPI(title='Stack Recommender', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend.router)
app.include_router(admin.router, prefix='/admin')


@app.get('/health')
def health():
    return {"status": "ok", "service": "stackx-backend"}
