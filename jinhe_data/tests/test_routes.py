from collections.abc import Iterable
from itertools import chain

from pytest import mark

from data import routes
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

    def flatten(stations_arr: Iterable[tuple[int, ...]]) -> set[int]:
        """Return a set of all stations."""
        return set(chain.from_iterable(filter(None, stations_arr)))

    assert (
        flatten(route.stations for route in routes)
        | flatten(route.up_stations for route in routes)
        | flatten(route.down_stations for route in routes)
        == station_ids
    )


@mark.parametrize("route", routes)
class TestRoute:
    """Check per route."""

    @staticmethod
    def test_name(route: Route):
        """The name is not empty."""
        assert route.name

    @staticmethod
    def test_stations(route: Route):
        """The station id is valid."""
        for stations in filter(
            None,
            (
                route.stations,
                route.up_stations,
                route.down_stations,
            ),
        ):
            assert set(stations) <= station_ids

    @staticmethod
    def test_services_time(route: Route):
        """The service time is valid."""
        for services in filter(
            None,
            (
                route.services,
                route.up_services,
                route.down_services,
            ),
        ):
            for service in services:
                for time in service:
                    h, m = map(int, time.split(":"))
                    assert 0 <= h < 24
                    assert 0 <= m < 60

    @staticmethod
    @mark.skip(reason="not implemented yet")
    def test_up_down(route: Route):
        """The route is up and down or none."""
        assert (
            route.stations is None
            and route.services is None
            and route.up_stations is not None
            and route.up_services is not None
            and route.down_stations is not None
            and route.down_services is not None
        ) or (
            route.stations is not None
            and route.services is not None
            and route.up_stations is None
            and route.up_services is None
            and route.down_stations is None
            and route.down_services is None
        )

    @staticmethod
    @mark.skip(reason="not implemented yet")
    def test_stations_services(route: Route):
        """The length of a service is equal to the number of the stations."""
        for stations, services in (
            (route.stations, route.services),
            (route.up_stations, route.up_services),
            (route.down_stations, route.down_services),
        ):
            if stations:
                for service in services:
                    assert len(service) == len(stations)
