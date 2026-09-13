from fastapi import HTTPException
from passlib.context import CryptContext

from app.core.security import create_access_token, verify_password
from app.models.farmer import Farmer
from app.repositories.farmer import FarmerRepository
from app.schemas.auth import (
    FarmerLogin,
    FarmerRegister,
    FarmerResponse,
    TokenResponse,
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class AuthService:

    def __init__(
        self,
        repository: FarmerRepository,
    ):
        self.repository = repository

    def register_farmer(
        self,
        data: FarmerRegister,
    ) -> FarmerResponse:

        existing_farmer = self.repository.get_by_phone(
            data.phone
        )

        if existing_farmer:
            raise HTTPException(
                status_code=409,
                detail="Phone number already registered",
            )

        hashed_password = pwd_context.hash(
            data.password
        )

        farmer = Farmer(
            name=data.name,
            phone=data.phone,
            password_hash=hashed_password,
            language=data.language,
        )

        created_farmer = self.repository.create(
            farmer
        )

        return FarmerResponse.model_validate(
            created_farmer
        )

    def login_farmer(
        self,
        data: FarmerLogin,
    ) -> TokenResponse:

        farmer = self.repository.get_by_phone(
            data.phone
        )

        if not farmer:
            raise HTTPException(
                status_code=401,
                detail="Invalid phone number or password",
            )

        if not verify_password(
            data.password,
            farmer.password_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid phone number or password",
            )

        access_token = create_access_token(
            farmer.id
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
        )