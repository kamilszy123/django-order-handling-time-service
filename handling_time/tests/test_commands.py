from datetime import date, timedelta

import pytest
from unittest.mock import patch
from django.core.management import call_command
from handling_time.models import Account, HandlingTimeConfig


@pytest.mark.django_db
@patch("handling_time.management.commands.update_handling_time.calculate_handling_time")
@patch("handling_time.management.commands.update_handling_time.update_handling_time")
def test_command_updates_offer(moc_update, moc_calc):
    moc_calc.return_value = "P3D"
    account = Account.objects.create(name="Allegro")

    HandlingTimeConfig.objects.create(
        account=account,
        offer_id="12345",
        target_date=date.today() + timedelta(days=3)
    )
    call_command("update_handling_time")

    moc_update.assert_called_once_with(
        account,
        "12345",
        "P3D"
    )
    moc_calc.assert_called_once_with(date.today() + timedelta(days=3))
