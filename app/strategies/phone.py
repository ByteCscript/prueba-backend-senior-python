from app.schemas import ApplicationCreate, ApplicationStatus
from app.strategies.base import CreditPolicy, EvaluationResult


class PhonePolicy(CreditPolicy):

    def evaluate(self, application: ApplicationCreate) -> EvaluationResult:
        rejection_reasons = []

        installment = application.amount / 12

        if application.external_score < 700:
            rejection_reasons.append("External score must be at least 700")

        if application.employment_months < 12:
            rejection_reasons.append("Employment must be at least 12 months")

        if installment > application.monthly_income * 0.25:
            rejection_reasons.append("Installment exceeds 25% of monthly income")

        status = (
            ApplicationStatus.REJECTED
            if rejection_reasons
            else ApplicationStatus.APPROVED
        )

        return EvaluationResult(
            status=status,
            rejection_reasons=rejection_reasons,
        )
