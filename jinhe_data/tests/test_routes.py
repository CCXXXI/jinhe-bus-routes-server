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
    @mark.skip(reason="not implemented yet")
    def test_stations_services(route: Route):
        """The route should be up and down or none."""
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
