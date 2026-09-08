from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_approved_phone_application():
    payload = {
        "amount": 1_200_000,
        "monthly_income": 4_000_000,
        "employment_months": 24,
        "external_score": 750,
        "product": "PHONE",
    }

    response = client.post("/applications", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["product"] == "PHONE"
    assert data["status"] == "APPROVED"
    assert data["rejection_reasons"] == []


def test_create_rejected_phone_application():
    payload = {
        "amount": 6_000_000,
        "monthly_income": 1_000_000,
        "employment_months": 6,
        "external_score": 650,
        "product": "PHONE",
    }

    response = client.post("/applications", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["product"] == "PHONE"
    assert data["status"] == "REJECTED"
    assert len(data["rejection_reasons"]) > 0


def test_get_application_by_id():
    payload = {
        "amount": 1_200_000,
        "monthly_income": 4_000_000,
        "employment_months": 24,
        "external_score": 750,
        "product": "PHONE",
    }

    create_response = client.post("/applications", json=payload)

    assert create_response.status_code == 201

    application_id = create_response.json()["id"]

    response = client.get(f"/applications/{application_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == application_id
    assert data["product"] == "PHONE"
    assert data["status"] == "APPROVED"


def test_get_application_not_found():
    response = client.get("/applications/999999")

    assert response.status_code == 404

    assert response.json() == {"detail": "Application not found"}


def test_list_applications_filtered_by_status_and_product():
    approved_twist_payload = {
        "amount": 1_200_000,
        "monthly_income": 2_000_000,
        "employment_months": 6,
        "external_score": 650,
        "product": "TWIST",
    }

    rejected_twist_payload = {
        "amount": 12_000_000,
        "monthly_income": 1_000_000,
        "employment_months": 6,
        "external_score": 550,
        "product": "TWIST",
    }

    client.post(
        "/applications",
        json=approved_twist_payload,
    )

    client.post(
        "/applications",
        json=rejected_twist_payload,
    )

    response = client.get(
        "/applications",
        params={
            "status": "APPROVED",
            "product": "TWIST",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    for application in data:
        assert application["status"] == "APPROVED"
        assert application["product"] == "TWIST"


def test_invalid_product_returns_422():
    payload = {
        "amount": 1_200_000,
        "monthly_income": 4_000_000,
        "employment_months": 24,
        "external_score": 750,
        "product": "INVALID_PRODUCT",
    }

    response = client.post("/applications", json=payload)

    assert response.status_code == 422


def test_invalid_amount_returns_422():
    payload = {
        "amount": 0,
        "monthly_income": 4_000_000,
        "employment_months": 24,
        "external_score": 750,
        "product": "PHONE",
    }

    response = client.post("/applications", json=payload)

    assert response.status_code == 422


def test_reevaluate_application():
    payload = {
        "amount": 1_200_000,
        "monthly_income": 4_000_000,
        "employment_months": 24,
        "external_score": 750,
        "product": "PHONE",
    }

    create_response = client.post("/applications", json=payload)

    assert create_response.status_code == 201

    application_id = create_response.json()["id"]

    response = client.post(f"/applications/{application_id}/reevaluate")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == application_id
    assert data["status"] == "APPROVED"
    assert data["product"] == "PHONE"
