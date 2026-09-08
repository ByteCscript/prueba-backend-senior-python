from app.schemas import ApplicationCreate, ApplicationStatus, ProductType
from app.strategies.factory import get_policy


def test_phone_application_is_approved():
    application = ApplicationCreate(
        amount=1_200_000,
        monthly_income=4_000_000,
        employment_months=24,
        external_score=750,
        product=ProductType.PHONE,
    )

    policy = get_policy(application.product)

    result = policy.evaluate(application)

    assert result.status == ApplicationStatus.APPROVED
    assert result.rejection_reasons == []


def test_phone_application_is_rejected():
    application = ApplicationCreate(
        amount=6_000_000,
        monthly_income=1_000_000,
        employment_months=6,
        external_score=650,
        product=ProductType.PHONE,
    )

    policy = get_policy(application.product)

    result = policy.evaluate(application)

    assert result.status == ApplicationStatus.REJECTED
    assert len(result.rejection_reasons) > 0


def test_twist_application_is_approved():
    application = ApplicationCreate(
        amount=1_200_000,
        monthly_income=2_000_000,
        employment_months=6,
        external_score=650,
        product=ProductType.TWIST,
    )

    policy = get_policy(application.product)

    result = policy.evaluate(application)

    assert result.status == ApplicationStatus.APPROVED


def test_twist_application_is_rejected():
    application = ApplicationCreate(
        amount=12_000_000,
        monthly_income=1_000_000,
        employment_months=6,
        external_score=550,
        product=ProductType.TWIST,
    )

    policy = get_policy(application.product)

    result = policy.evaluate(application)

    assert result.status == ApplicationStatus.REJECTED


def test_card_application_is_approved():
    application = ApplicationCreate(
        amount=10_000_000,
        monthly_income=2_000_000,
        employment_months=1,
        external_score=560,
        product=ProductType.CARD,
    )

    policy = get_policy(application.product)

    result = policy.evaluate(application)

    assert result.status == ApplicationStatus.APPROVED


def test_card_application_is_rejected():
    application = ApplicationCreate(
        amount=1_000_000,
        monthly_income=2_000_000,
        employment_months=24,
        external_score=490,
        product=ProductType.CARD,
    )

    policy = get_policy(application.product)

    result = policy.evaluate(application)

    assert result.status == ApplicationStatus.REJECTED
