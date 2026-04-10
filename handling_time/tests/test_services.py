from datetime import date, timedelta

from handling_time.services import calculate_handling_time


def test_handling_time_1_day():
    target_date = date.today() + timedelta(days=1)

    result = calculate_handling_time(target_date)

    assert result == "PT24H"

def test_handling_time_12_days():
    target_date = date.today() + timedelta(days=12)

    result = calculate_handling_time(target_date)

    assert result == "P14D"

def test_handling_time_past_date():
    target_date =date.today() - timedelta(days=1)

    result = calculate_handling_time(target_date)

    assert result == "PT24H"