from datetime import date, timedelta

from app.schemas.filter_schema import FilterBase2


def test_filter_base2_defaults_are_computed_at_request_time() -> None:
    f = FilterBase2()
    assert f.time_end == date.today()
    assert f.time_start == date.today() - timedelta(days=7)
