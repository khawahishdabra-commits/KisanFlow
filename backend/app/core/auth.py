from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.farmer import Farmer
from app.repositories.farmer import FarmerRepository


security = HTTPBearer()


def get_current_farmer(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db),
) -> Farmer:

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        farmer_id = payload.get("sub")

        if farmer_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

        farmer_id = int(farmer_id)

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    repository = FarmerRepository(db)

    farmer = repository.get_by_id(farmer_id)

    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Farmer not found",
        )

    return farmer