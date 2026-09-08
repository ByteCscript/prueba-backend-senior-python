from sqlalchemy import Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    amount: Mapped[int] = mapped_column(Integer, nullable=False)

    monthly_income: Mapped[int] = mapped_column(Integer, nullable=False)

    employment_months: Mapped[int] = mapped_column(Integer, nullable=False)

    external_score: Mapped[int] = mapped_column(Integer, nullable=False)

    product: Mapped[str] = mapped_column(String, nullable=False)

    status: Mapped[str] = mapped_column(String, nullable=False)

    rejection_reasons: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=list
    )
