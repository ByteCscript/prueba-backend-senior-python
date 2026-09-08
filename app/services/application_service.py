from app.models import Application
from app.repositories.application_repository import ApplicationRepository
from app.strategies.factory import get_policy
from app.schemas import ApplicationCreate, ProductType


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

    def reevaluate_application(
        self,
        application_id: int,
    ) -> Application | None:

        application = self.repository.get_by_id(application_id)

        if application is None:
            return None

        data = ApplicationCreate(
            amount=application.amount,
            monthly_income=application.monthly_income,
            employment_months=application.employment_months,
            external_score=application.external_score,
            product=ProductType(application.product),
        )

        policy = get_policy(data.product)
        evaluation = policy.evaluate(data)

        application.status = evaluation.status.value
        application.rejection_reasons = evaluation.rejection_reasons

        return self.repository.update(application)
