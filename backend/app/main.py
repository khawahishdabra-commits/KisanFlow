from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.routers.crop import router as crop_router
from app.routers.centre import router as centre_router
from app.routers.intelligence import router as intelligence_router
from app.routers.booking import router as booking_router
from app.routers.auth import router as auth_router
from app.routers.farmer import router as farmer_router
from app.routers.recommendation import router as recommendation_router
from app.routers.operator import router as operator_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="KisanFlow API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://kisan-flow-eight.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(crop_router)
app.include_router(centre_router)
app.include_router(intelligence_router)
app.include_router(booking_router)
app.include_router(auth_router)
app.include_router(farmer_router)
app.include_router(recommendation_router)
app.include_router(operator_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/health/db")
def database_health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected"
    }

