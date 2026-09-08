from app.schemas import ApplicationCreate, ApplicationStatus
from app.strategies.base import CreditPolicy, EvaluationResult


class TwistPolicy(CreditPolicy):

    def evaluate(self, application: ApplicationCreate) -> EvaluationResult:
        rejection_reasons = []

        installment = application.amount / 12

        if application.external_score < 600:
            rejection_reasons.append("External score must be at least 600")

        if installment > application.monthly_income * 0.35:
            rejection_reasons.append("Installment exceeds 35% of monthly income")

        status = (
            ApplicationStatus.REJECTED
            if rejection_reasons
            else ApplicationStatus.APPROVED
        )

        return EvaluationResult(
            status=status,
            rejection_reasons=rejection_reasons,
        )
