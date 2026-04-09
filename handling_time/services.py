from datetime import date, datetime

ALLOWED_HANDLING_TIMES = [
    (1, "PT24H"),
    (2, "P2D"),
    (3, "P3D"),
    (4, "P4D"),
    (5, "P5D"),
    (7, "P7D"),
    (10, "P10D"),
    (14, "P14D"),
    (21, "P21D"),
    (30, "P30D"),
    (60, "P60D")
]
MIN_HANDLING_TIME = "PT24H"
MAX_HANDLING_TIME = "P60D"


def calculate_handling_time(target_date):
    if isinstance(target_date, datetime):
        target_date = target_date.date()

    if not isinstance(target_date, date):
        raise ValueError("target_date must be a date")

    today = date.today()

    delta_days = (target_date - today).days

    if delta_days < 1:
        return MIN_HANDLING_TIME

    for days, code in ALLOWED_HANDLING_TIMES:
        if delta_days <= days:
            return code

    return MAX_HANDLING_TIME
