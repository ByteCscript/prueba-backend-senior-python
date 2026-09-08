from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.application_repository import ApplicationRepository
from app.schemas import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatus,
    ProductType,
)
from app.services.application_service import ApplicationService

router = APIRouter(
    prefix="/applications",
    tags=["applications"],
)


def get_service(
    db: Session = Depends(get_db),
) -> ApplicationService:

    repository = ApplicationRepository(db)

    return ApplicationService(repository)


@router.post(
    "",
    response_model=ApplicationResponse,
    status_code=201,
)
def create_application(
    data: ApplicationCreate,
    service: ApplicationService = Depends(get_service),
):
    return service.create_application(data)


@router.post(
    "/{application_id}/reevaluate",
    response_model=ApplicationResponse,
)
def reevaluate_application(
    application_id: int,
    service: ApplicationService = Depends(get_service),
):
    application = service.reevaluate_application(application_id)

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return application


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def get_application(
    application_id: int,
    service: ApplicationService = Depends(get_service),
):
    application = service.get_application(application_id)

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return application


@router.get(
    "",
    response_model=list[ApplicationResponse],
)
def list_applications(
    status: ApplicationStatus | None = None,
    product: ProductType | None = None,
    service: ApplicationService = Depends(get_service),
):
    return service.list_applications(
        status=status.value if status else None,
        product=product.value if product else None,
    )
