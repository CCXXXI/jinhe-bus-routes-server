from pytest import mark

from src.data import stations
from src.data_types import Station

station_ids = {station.id for station in stations}


def test_id():
    """The id is unique."""
    assert len(station_ids) == len(stations)


@mark.parametrize("station", stations)
class TestStation:
    """Check per station."""

    @staticmethod
    def test_id(station: Station):
        """The id is a positive number."""
        assert int(station.id.removeprefix("_")) > 0
