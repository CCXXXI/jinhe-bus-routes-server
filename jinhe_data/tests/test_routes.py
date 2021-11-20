from pytest import mark

from data import routes
from src.data_types import Route


def test_name():
    """The name is unique."""
    assert len({route.name for route in routes}) == len(routes)


def test_length():
    """There are 93 routes."""
    assert len(routes) == 93


@mark.parametrize("route", routes)
class TestRoute:
    """Check per route."""

    @staticmethod
    def test_name(route: Route):
        """The name is not empty."""
        assert route.name

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
    def test_services_ascending(route: Route):
        """The service time is ascending."""
        for services in filter(
            None,
            (
                route.services,
                route.up_services,
                route.down_services,
            ),
        ):
            for service in services:
                assert service == tuple(sorted(service))

    @staticmethod
    @mark.skip(reason="not implemented yet")
    def test_stations_services(route: Route):
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
            and route.services is None
            and route.down_stations is None
            and route.down_services is None
        )

    @staticmethod
    @mark.skip(reason="not implemented yet")
    def test_stations_services_length(route: Route):
        """The length of a service is equal to the number of the stations."""
        for stations, services in (
            (route.stations, route.services),
            (route.up_stations, route.up_services),
            (route.down_stations, route.down_services),
        ):
            if stations:
                for service in services:
                    assert len(service) == len(stations)
