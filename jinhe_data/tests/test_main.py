from data import stations
from src.main import g, r, save


def test_save():
    """Save all data to the database."""
    assert not r.hgetall("route:1")
    assert g.query("MATCH (p) RETURN count(p)").result_set[0][0] == 0

    save()

    assert r.hgetall("route:1")
    assert g.query("MATCH (p) RETURN count(p)").result_set[0][0] == len(stations)
