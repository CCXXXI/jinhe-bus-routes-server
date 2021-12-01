from collections.abc import Iterable
from itertools import chain

from pytest import mark

from src.data import routes
from src.data_types import Route
from .test_stations import station_ids


def test_name():
    """The name is unique."""
    assert len({route.name for route in routes}) == len(routes)


def test_length():
    """There are 93 routes."""
    assert len(routes) == 93


def test_stations():
    """No isolated station."""

    def flatten(stations_arr: Iterable[tuple[str, ...]]) -> set[str]:
        """Return a set of all stations."""
        return set(chain.from_iterable(filter(None, stations_arr)))

    assert (
        flatten(route.stations for route in routes)
        | flatten(route.u_stations for route in routes)
        | flatten(route.d_stations for route in routes)
        == station_ids
    )


@mark.parametrize("r", routes)
class TestRoute:
    """Check per route."""

    @staticmethod
    def test_name(r: Route):
        """The name is not empty."""
        assert r.name

    @staticmethod
    def test_stations(r: Route):
        """The station id is valid and unique."""
        for stations in filter(None, (r.stations, r.u_stations, r.d_stations)):
            assert set(stations) <= station_ids
            assert len(stations) == len(set(stations))

    @staticmethod
    def test_service_time(r: Route):
        """The time is valid and unique."""
        for first in filter(None, (r.first, r.u_first, r.d_first)):
            for time in first:
                assert 0 <= time < 24 * 60
            assert len(first) == len(set(first))

    @staticmethod
    def test_step(r: Route):
        """The step is valid, unique and ascending."""
        for steps in filter(None, (r.steps, r.u_steps, r.d_steps)):
            for step in steps:
                assert 0 <= step < 24 * 60
            assert len(steps) == len(set(steps))
            assert steps == tuple(sorted(steps))

    @staticmethod
    def test_directional(r: Route):
        """The route is directional or not."""
        assert (
            r.directional
            and r.stations is None
            and r.first is None
            and r.steps is None
            and r.u_stations is not None
            and r.u_first is not None
            and r.u_steps is not None
            and r.d_stations is not None
            and r.d_first is not None
            and r.d_steps is not None
        ) or (
            not r.directional
            and r.stations is not None
            and r.first is not None
            and r.steps is not None
            and r.u_stations is None
            and r.u_first is None
            and r.u_steps is None
            and r.d_stations is None
            and r.d_first is None
            and r.d_steps is None
        )

    @staticmethod
    def test_stations_services(r: Route):
        """The length of the first service is equal to the number of the stations."""
        for stations, first in (
            (r.stations, r.first),
            (r.u_stations, r.u_first),
            (r.d_stations, r.d_first),
        ):
            if stations:
                assert len(first) == len(stations)
