from fastapi import FastAPI

from app.database import Base, engine
from app.routers.applications import router as applications_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Credit Evaluation Service")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(applications_router)
