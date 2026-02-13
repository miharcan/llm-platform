from fastapi import FastAPI
from app.api.routes import router
from app.middleware.request_id import add_request_id
from app.db.database import engine
from app.db.models import Base

app = FastAPI(title="LLM Platform Blueprint")
app.middleware("http")(add_request_id)

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}

