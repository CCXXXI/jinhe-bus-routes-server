from pytest import mark

from data import stations
from src.data_types import Station


def test_id():
    """The id is unique."""
    assert len({station.id for station in stations}) == len(stations)


@mark.parametrize("station", stations)
class TestStation:
    """Check per station."""

    @staticmethod
    def test_id(station: Station):
        """The id is a positive number."""
        assert station.id > 0
