from src.data import stations
from src.main import g, r, save


def test_save():
    """Save all data to the database."""
    assert not r.get("version")
    assert not r.hgetall("Route:_1")
    assert g.query("MATCH (p) RETURN count(p)").result_set[0][0] == 0
    assert not g.query("MATCH (:_41394)-[r:_43d]->(:_4989) RETURN r").result_set

    save()

    assert len(r.get("version")) == 40  # A Git commit ID is a 40 digits long SHA-1 hash
    assert r.hgetall("Route:_1")["type"] == "干线"
    assert g.query("MATCH (p) RETURN count(p)").result_set[0][0] == len(stations)
    assert (
        g.query("MATCH (:_41394)-[r:_43d]->(:_4989) RETURN r").result_set[0][0].relation
        == "_43d"
    )
