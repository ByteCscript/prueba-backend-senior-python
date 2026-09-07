from enum import Enum

from pydantic import BaseModel, Field


class ProductType(str, Enum):
    PHONE = "PHONE"
    TWIST = "TWIST"
    CARD = "CARD"


class ApplicationStatus(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ApplicationCreate(BaseModel):
    amount: int = Field(gt=0)
    monthly_income: int = Field(gt=0)
    employment_months: int = Field(ge=0)
    external_score: int = Field(ge=0, le=1000)
    product: ProductType


class ApplicationResponse(BaseModel):
    id: int
    amount: int
    monthly_income: int
    employment_months: int
    external_score: int
    product: ProductType
    status: ApplicationStatus
    rejection_reasons: list[str]

    model_config = {
        "from_attributes": True
    }