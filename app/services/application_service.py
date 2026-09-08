from app.models import Application
from app.repositories.application_repository import ApplicationRepository
from app.schemas import ApplicationCreate
from app.strategies.factory import get_policy


class ApplicationService:

    def __init__(self, repository: ApplicationRepository):
        self.repository = repository

    def create_application(
        self,
        data: ApplicationCreate,
    ) -> Application:

        policy = get_policy(data.product)

        evaluation = policy.evaluate(data)

        application = Application(
            amount=data.amount,
            monthly_income=data.monthly_income,
            employment_months=data.employment_months,
            external_score=data.external_score,
            product=data.product.value,
            status=evaluation.status.value,
            rejection_reasons=evaluation.rejection_reasons,
        )

        return self.repository.create(application)

    def get_application(
        self,
        application_id: int,
    ) -> Application | None:

        return self.repository.get_by_id(application_id)

    def list_applications(
        self,
        status: str | None = None,
        product: str | None = None,
    ) -> list[Application]:

        return self.repository.list(
            status=status,
            product=product,
        )
