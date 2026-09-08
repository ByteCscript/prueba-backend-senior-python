"""Archivo de politicas para sepáracion if else"""

from app.schemas import ProductType
from app.strategies.base import CreditPolicy
from app.strategies.card import CardPolicy
from app.strategies.phone import PhonePolicy
from app.strategies.twist import TwistPolicy

_POLICIES: dict[ProductType, CreditPolicy] = {
    ProductType.PHONE: PhonePolicy(),
    ProductType.TWIST: TwistPolicy(),
    ProductType.CARD: CardPolicy(),
}


def get_policy(product: ProductType) -> CreditPolicy:
    return _POLICIES[product]
