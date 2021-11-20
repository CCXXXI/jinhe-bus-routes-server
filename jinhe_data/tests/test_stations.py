from pytest import mark

from data import stations
from src.data_types import Station


def test_id():
    """id is unique"""
    assert len({station.id for station in stations}) == len(stations)


@mark.parametrize("station", stations)
class TestStation:
    """Check per station."""

    def test_id(self, station: Station):
        """id > 0"""
        assert station.id > 0
