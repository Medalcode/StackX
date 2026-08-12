import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from . import sanity_sync
from .database import engine
from .models import Base
from .routes import admin, recommend
from .sanity_sync import start_scheduler

logger = logging.getLogger("stackx.main")

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    Base.metadata.create_all(bind=engine)
    if os.getenv('SANITY_PROJECT_ID'):
        try:
            sanity_sync.sync()
        except Exception as e:
            logger.error("Sanity sync failed on startup: %s", e)
        if os.getenv('ENABLE_IN_PROCESS_SCHEDULER', 'false').lower() == 'true':
            try:
                start_scheduler(sanity_sync.sync)
            except Exception as e:
                logger.error("Scheduler start failed: %s", e)
    yield



app = FastAPI(title='Stack Recommender', lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
