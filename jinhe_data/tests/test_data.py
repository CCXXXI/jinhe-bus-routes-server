from data.routes import routes


def test_routes():
    """Check routes data."""
    # `directional` is True of False
    assert all(route.directional in (0, 1) for route in routes)

    # `name` is unique
    assert len({route.name for route in routes}) == len(routes)
