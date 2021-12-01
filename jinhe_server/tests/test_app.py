from src.app import app

c = app.test_client()


def test_version():
    """The Git commit ID is a 40 digits long SHA-1 hash."""
    assert len(c.get("/version").data) == 40


def test_routes():
    """UC-1"""
    assert c.get("/routes/").json["30"] == "1"
    assert c.get("/routes/30").json == {
        "direction": "燎原-北路湾公交站",
        "oneway": "约49分",
        "kilometer": "12.0",
        "runtime": "6:30-22:30",
        "interval": "8",
        "type": "干线",
    }


def test_stations():
    """UC-2"""
    stations = c.get("/stations/").json
    assert {"id": "7542", "zh": "兴义镇(始发站)", "en": "XingYiZhen"} in stations
    assert {"id": "7527", "zh": "永盛(始发站)", "en": "YongSheng"} in stations
    assert {"id": "14495", "zh": "火车西站公交站(终点站)", "en": "Huo Che Zhan"} in stations

    stations_2u = c.get("/routes/2u/stations").json
    assert stations_2u[0] == "7542"
    assert stations_2u[1] == "7527"
    assert stations_2u[-1] == "14495"
    assert len(stations_2u) == 28
