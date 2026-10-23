from datetime import date, timedelta

import pytest

from app.helpers.core_helper import (
    calculate_next_recharge,
    calculate_recharge_percentage,
    calculate_trash_cleaning_next_time,
    calculate_trash_cleaning_percentage,
)

PCT_0 = 0.0
PCT_50 = 50.0
PCT_100 = 100.0

# --------------- calculate_next_recharge ---------------


def test_next_recharge_empty_list():
    assert calculate_next_recharge([]) is None


def test_next_recharge_single_date():
    assert calculate_next_recharge([date(2026, 1, 10)]) is None


def test_next_recharge_two_dates_mean():
    dates = [date(2026, 1, 1), date(2026, 1, 11)]
    assert calculate_next_recharge(dates, "media") == date(2026, 1, 21)


def test_next_recharge_two_dates_median():
    dates = [date(2026, 1, 1), date(2026, 1, 11)]
    assert calculate_next_recharge(dates, "mediana") == date(2026, 1, 21)


def test_next_recharge_descending_order():
    """Bug 1: dates from extract_dates_recharge come in DESC order."""
    dates = [date(2026, 3, 1), date(2026, 2, 1), date(2026, 1, 1)]
    result = calculate_next_recharge(dates, "media")
    # Intervals: 31, 28 → mean ~29.5 → int 29
    expected = date(2026, 3, 1) + timedelta(days=29)
    assert result == expected


def test_next_recharge_duplicate_dates():
    dates = [date(2026, 1, 1), date(2026, 1, 1), date(2026, 1, 11)]
    assert calculate_next_recharge(dates, "media") == date(2026, 1, 21)


def test_next_recharge_invalid_type_raises():
    dates = [date(2026, 1, 1), date(2026, 1, 11)]
    with pytest.raises(ValueError, match="type deve ser"):
        calculate_next_recharge(dates, "invalid")


def test_next_recharge_three_dates_median():
    dates = [date(2026, 1, 1), date(2026, 1, 11), date(2026, 1, 31)]
    # Intervals: 10, 20 → median 15
    assert calculate_next_recharge(dates, "mediana") == date(2026, 2, 15)


# --------------- calculate_recharge_percentage ---------------


def test_recharge_pct_empty_list():
    assert calculate_recharge_percentage([]) == 0.0


def test_recharge_pct_single_date():
    assert calculate_recharge_percentage([date(2026, 1, 1)]) == 0.0


def test_recharge_pct_just_recharged():
    """today == last recharge → 100%"""
    today = date(2026, 5, 10)
    dates = [date(2026, 4, 10), date(2026, 5, 10)]
    assert calculate_recharge_percentage(dates, today=today) == PCT_100


def test_recharge_pct_halfway():
    """Half interval elapsed → 50%"""
    today = date(2026, 5, 25)
    dates = [date(2026, 4, 10), date(2026, 5, 10)]
    assert calculate_recharge_percentage(dates, today=today) == PCT_50


def test_recharge_pct_full_interval():
    """Full interval elapsed → 0%"""
    today = date(2026, 6, 9)
    dates = [date(2026, 4, 10), date(2026, 5, 10)]
    assert calculate_recharge_percentage(dates, today=today) == 0.0


def test_recharge_pct_over_interval_clamped():
    """More than interval → clamped to 0%"""
    today = date(2026, 7, 10)
    dates = [date(2026, 4, 10), date(2026, 5, 10)]
    assert calculate_recharge_percentage(dates, today=today) == 0.0


def test_recharge_pct_descending_order():
    today = date(2026, 5, 10)
    dates = [date(2026, 5, 10), date(2026, 4, 10)]
    assert calculate_recharge_percentage(dates, today=today) == PCT_100


def test_recharge_pct_duplicates_no_positive_interval():
    today = date(2026, 5, 10)
    dates = [date(2026, 5, 10), date(2026, 5, 10)]
    assert calculate_recharge_percentage(dates, today=today) == 0.0


# --------------- calculate_trash_cleaning_next_time ---------------


def test_trash_next_empty_list():
    assert calculate_trash_cleaning_next_time([]) is None


def test_trash_next_single_date():
    assert calculate_trash_cleaning_next_time([date(2026, 1, 10)]) is None


def test_trash_next_two_dates():
    dates = [date(2026, 1, 1), date(2026, 1, 11)]
    assert calculate_trash_cleaning_next_time(dates) == date(2026, 1, 21)


def test_trash_next_descending_order():
    dates = [date(2026, 3, 1), date(2026, 2, 1), date(2026, 1, 1)]
    expected = date(2026, 3, 1) + timedelta(days=29)
    assert calculate_trash_cleaning_next_time(dates) == expected


def test_trash_next_duplicates():
    dates = [date(2026, 1, 1), date(2026, 1, 1), date(2026, 1, 11)]
    assert calculate_trash_cleaning_next_time(dates) == date(2026, 1, 21)


# --------------- calculate_trash_cleaning_percentage ---------------


def test_trash_pct_empty_list():
    assert calculate_trash_cleaning_percentage([]) == 0.0


def test_trash_pct_single_date():
    assert calculate_trash_cleaning_percentage([date(2026, 1, 1)]) == 0.0


def test_trash_pct_just_cleaned():
    """today == last cleaning → 0% (just cleaned)"""
    today = date(2026, 5, 10)
    dates = [date(2026, 4, 10), date(2026, 5, 10)]
    assert calculate_trash_cleaning_percentage(dates, today=today) == 0.0


def test_trash_pct_halfway():
    today = date(2026, 5, 25)
    dates = [date(2026, 4, 10), date(2026, 5, 10)]
    assert calculate_trash_cleaning_percentage(dates, today=today) == PCT_50


def test_trash_pct_full_interval():
    today = date(2026, 6, 9)
    dates = [date(2026, 4, 10), date(2026, 5, 10)]
    assert calculate_trash_cleaning_percentage(dates, today=today) == PCT_100


def test_trash_pct_over_interval_clamped():
    today = date(2026, 7, 10)
    dates = [date(2026, 4, 10), date(2026, 5, 10)]
    assert calculate_trash_cleaning_percentage(dates, today=today) == PCT_100


def test_trash_pct_descending_order():
    today = date(2026, 5, 10)
    dates = [date(2026, 5, 10), date(2026, 4, 10)]
    assert calculate_trash_cleaning_percentage(dates, today=today) == 0.0


def test_trash_pct_duplicates_no_positive_interval():
    today = date(2026, 5, 10)
    dates = [date(2026, 5, 10), date(2026, 5, 10)]
    assert calculate_trash_cleaning_percentage(dates, today=today) == 0.0
