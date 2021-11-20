from data import routes, stations


def test_routes():
    """Check routes data."""
    # `name` is unique
    assert len({route.name for route in routes}) == len(routes)

    # stations & services
    assert all(
        (
            route.stations is None
            and route.services is None
            and route.up_stations is not None
            and route.up_services is not None
            and route.down_stations is not None
            and route.down_services is not None
        )
        or (
            route.stations is not None
            and route.services is not None
            and route.up_stations is None
            and route.services is None
            and route.down_stations is None
            and route.down_services is None
        )
        for route in routes
    )

    # 93 routes
    assert len(routes) == 93


def test_stations():
    """Check stations data."""
    # id > 0
    assert all(station.id > 0 for station in stations)

    # id is unique
    assert len({station.id for station in stations}) == len(stations)
