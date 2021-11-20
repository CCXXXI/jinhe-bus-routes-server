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
        """The station id is valid and unique."""
        for stations in filter(
            None,
            (route.stations, route.up_stations, route.down_stations),
        ):
            assert set(stations) <= station_ids
            assert len(stations) == len(set(stations))

    @staticmethod
    def test_service_time(route: Route):
        """The time is valid and unique."""
        for service in filter(
            None,
            (route.first_service, route.first_up_service, route.first_down_service),
        ):
            for time in service:
                assert 0 <= time < 24 * 60
            assert len(service) == len(set(service))

    @staticmethod
    def test_step(route: Route):
        """The step is valid, unique and ascending."""
        for steps in filter(
            None,
            (route.steps, route.up_steps, route.down_steps),
        ):
            for step in steps:
                assert 0 <= step < 24 * 60
            assert len(steps) == len(set(steps))
            assert steps == tuple(sorted(steps))

    @staticmethod
    def test_up_down(route: Route):
        """The route is up and down or none."""
        assert (
            route.stations is None
            and route.first_service is None
            and route.steps is None
            and route.up_stations is not None
            and route.first_up_service is not None
            and route.up_steps is not None
            and route.down_stations is not None
            and route.first_down_service is not None
            and route.down_steps is not None
        ) or (
            route.stations is not None
            and route.first_service is not None
            and route.steps is not None
            and route.up_stations is None
            and route.first_up_service is None
            and route.up_steps is None
            and route.down_stations is None
            and route.first_down_service is None
            and route.down_steps is None
        )

    @staticmethod
    def test_stations_services(route: Route):
        """The length of the service is equal to the number of the stations."""
        for stations, service in (
            (route.stations, route.first_service),
            (route.up_stations, route.first_up_service),
            (route.down_stations, route.first_down_service),
        ):
            if stations:
                assert len(service) == len(stations)
