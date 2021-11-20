from data import stations


def test_stations():
    """Check stations data."""
    # id > 0
    assert all(station.id > 0 for station in stations)

    # id is unique
    assert len({station.id for station in stations}) == len(stations)
