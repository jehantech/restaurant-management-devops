from fastapi import FastAPI

from .database import Base, engine
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant Management System",
    description="Restaurant Management Service for DevOps Project",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Restaurant Management Service is running",
        "version": "1.0.0"
    }
