from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Application


class ApplicationRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, application: Application) -> Application:
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application

    def get_by_id(self, application_id: int) -> Application | None:
        statement = select(Application).where(Application.id == application_id)

        return self.db.scalar(statement)

    def list(
        self,
        status: str | None = None,
        product: str | None = None,
    ) -> list[Application]:

        statement = select(Application)

        if status:
            statement = statement.where(Application.status == status)

        if product:
            statement = statement.where(Application.product == product)

        return list(self.db.scalars(statement).all())

    def update(self, application: Application) -> Application:
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application
