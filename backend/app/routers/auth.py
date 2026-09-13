from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.farmer import FarmerRepository
from app.schemas.auth import FarmerRegister, FarmerResponse
from app.services.auth import AuthService
from app.schemas.auth import (
    FarmerLogin,
    FarmerRegister,
    FarmerResponse,
    TokenResponse,
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:
    repository = FarmerRepository(db)

    return AuthService(repository)


@router.post(
    "/register",
    response_model=FarmerResponse,
    status_code=201,
)
def register_farmer(
    data: FarmerRegister,
    service: AuthService = Depends(
        get_auth_service
    ),
):
    return service.register_farmer(data)

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_farmer(
    data: FarmerLogin,
    service: AuthService = Depends(
        get_auth_service
    ),
):
    return service.login_farmer(data)