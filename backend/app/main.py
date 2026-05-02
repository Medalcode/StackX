from fastapi import FastAPI
from .database import engine
from .models import Base
from .routes import recommend, admin

app = FastAPI(title='Stack Recommender')

app.include_router(recommend.router)
app.include_router(admin.router, prefix='/admin')


@app.on_event('startup')
def on_startup():
    # Create tables if they don't exist (development convenience).
    # In production, run migrations with Alembic before starting the service.
    Base.metadata.create_all(bind=engine)
