from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.schemas import ApplicationCreate, ApplicationStatus


@dataclass
class EvaluationResult:
    status: ApplicationStatus
    rejection_reasons: list[str]


class CreditPolicy(ABC):

    @abstractmethod
    def evaluate(self, application: ApplicationCreate) -> EvaluationResult:
        pass
