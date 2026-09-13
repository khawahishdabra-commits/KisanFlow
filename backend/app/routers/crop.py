from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.crop import CropRepository
from app.schemas.crop import CropResponse
from app.services.crop import CropService


router = APIRouter(
    prefix="/api/crops",
    tags=["Crops"],
)


def get_crop_service(
    db: Session = Depends(get_db),
) -> CropService:
    repository = CropRepository(db)

    return CropService(repository)


@router.get(
    "",
    response_model=list[CropResponse],
)
def get_crops(
    service: CropService = Depends(get_crop_service),
):
    return service.get_all_crops()