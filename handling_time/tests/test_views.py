import pytest
from rest_framework.test import APIClient

from handling_time.models import Account, HandlingTimeConfig


@pytest.mark.django_db
def test_create_handling_time_config():
    client = APIClient()

    Account.objects.create(name="Allegro")

    data = {
        "offer_id": "12345",
        "target_date": "2026-04-11"
    }

    response = client.post("/config/", data)

    assert response.status_code == 200
    assert response.data["offer_id"] == "12345"
    assert HandlingTimeConfig.objects.count() == 1


@pytest.mark.django_db
def test_create_handling_time_config_without_account():
    client = APIClient()
    data = {
        "offer_id": "12345",
        "target_date": "2026-04-11"
    }

    response = client.post("/config/", data)

    assert response.status_code == 400

@pytest.mark.django_db
def test_update_existing_handling_time_config():
    client = APIClient()

    account = Account.objects.create(name="Allegro")

    HandlingTimeConfig.objects.create(
        account=account,
        offer_id="12345",
        target_date="2026-04-11"
    )

    data = {
        "offer_id": "12345",
        "target_date": "2026-04-13"
    }

    response = client.post("/config/", data)

    assert response.data["status"] == "updated"
    assert response.status_code == 200
    assert HandlingTimeConfig.objects.count() == 1