from app.schemas import ApplicationCreate, ApplicationStatus
from app.strategies.base import CreditPolicy, EvaluationResult


class CardPolicy(CreditPolicy):

    def evaluate(self, application: ApplicationCreate) -> EvaluationResult:
        approved = application.external_score >= 550 or (
            application.external_score >= 500
            and application.monthly_income >= 3_000_000
        )

        rejection_reasons = []

        if not approved:
            rejection_reasons.append("Application does not meet CARD credit policy")

        status = ApplicationStatus.APPROVED if approved else ApplicationStatus.REJECTED

        return EvaluationResult(
            status=status,
            rejection_reasons=rejection_reasons,
        )
