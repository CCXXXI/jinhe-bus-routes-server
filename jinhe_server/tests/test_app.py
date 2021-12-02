from src.app import app

c = app.test_client()


def test_version():
    """The Git commit ID is a 40 digits long SHA-1 hash."""
    assert len(c.get("/version").data) == 40


def test_uc1():
    """查询某条线路的基本信息。"""
    assert c.get("/routes/").json["30"] == "1"
    assert c.get("/routes/30").json == {
        "direction": "燎原-北路湾公交站",
        "oneway": "约49分",
        "kilometer": "12.0",
        "runtime": "6:30-22:30",
        "interval": "8",
        "type": "干线",
    }


def test_uc2():
    """查询某条线路方向的全部站点信息。"""
    stations = c.get("/stations/").json
    assert {"id": "7542", "zh": "兴义镇(始发站)", "en": "XingYiZhen"} in stations
    assert {"id": "7527", "zh": "永盛(始发站)", "en": "YongSheng"} in stations
    assert {"id": "14495", "zh": "火车西站公交站(终点站)", "en": "Huo Che Zhan"} in stations

    first = c.get("/routes/2u/first").json
    assert first[0][0] == "7542"
    assert first[1][0] == "7527"
    assert first[-1][0] == "14495"
    assert len(first) == 28


def test_uc3():
    """查询锦城广场站停靠的所有线路。"""
    stations = c.get("/stations/").json
    assert set(s["id"] for s in stations if s["zh"] == "锦城广场") == {
        "58290",
        "64355",
        "58289",
        "64356",
    }

    assert {n for n, _ in c.get("/stations/58290/first").json} == {
        "K5u",
    }
    assert {n for n, _ in c.get("/stations/64355/first").json} == {
        "N26d",
        "G33u",
        "17d",
    }
    assert {n for n, _ in c.get("/stations/58289/first").json} == {
        "K5d",
    }
    assert {n for n, _ in c.get("/stations/64356/first").json} == {
        "N26u",
        "G33d",
        "17u",
    }
