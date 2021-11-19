from data.routes import routes


def test_routes():
    """Check routes data."""
    # `directional` is True of False
    assert all(route.directional in (0, 1) for route in routes)

    # `name` is unique
    assert len({route.name for route in routes}) == len(routes)

    # stations
    assert all(
        (
            route.stations is None
            and route.up_stations is not None
            and route.down_stations is not None
        )
        or (
            route.stations is not None
            and route.up_stations is None
            and route.down_stations is None
        )
        for route in routes
    )

    # 93 routes
    assert len(routes) == 93
