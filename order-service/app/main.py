from fastapi import FastAPI

from .database import Base, engine
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant Order Service",
    description="Order Management Service for Restaurant Management System",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Order Service is running",
        "version": "1.0.0"
    }
