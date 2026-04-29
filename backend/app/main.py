import os

from fastapi import FastAPI

from . import sanity_sync
from .database import engine
from .models import Base
from .routes import admin, recommend
from .sanity_sync import start_scheduler

app = FastAPI(title='Stack Recommender')

app.include_router(recommend.router)
app.include_router(admin.router, prefix='/admin')


@app.on_event('startup')
def on_startup():
    # Create tables if they don't exist (development)
    Base.metadata.create_all(bind=engine)
    # Start periodic sanity sync if SANITY_PROJECT_ID is configured
    if os.getenv('SANITY_PROJECT_ID'):
        # run an immediate sync at startup
        try:
            sanity_sync.sync()
        except Exception:
            pass
        # schedule periodic sync
        try:
            start_scheduler(sanity_sync.sync)
        except Exception:
            pass
