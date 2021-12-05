from . import c


def test_version():
    """The Git commit ID is a 40 digits long SHA-1 hash."""
    assert len(c.get("/jinhe/meta/version").data) == 40


def test_uc1():
    """查询某条线路的基本信息。"""
    assert c.get("/jinhe/routes/").json["30"] == "1"
    assert c.get("/jinhe/routes/30").json == {
        "direction": "燎原-北路湾公交站",
        "oneway": "约49分",
        "kilometer": "12.0",
        "runtime": "6:30-22:30",
        "interval": "8",
        "type": "干线",
    }


def test_uc2():
    """查询某条线路方向的全部站点信息。"""
    stations = c.get("/jinhe/stations/").json
    assert {"id": "7542", "zh": "兴义镇(始发站)", "en": "XingYiZhen"} in stations
    assert {"id": "7527", "zh": "永盛(始发站)", "en": "YongSheng"} in stations
    assert {"id": "14495", "zh": "火车西站公交站(终点站)", "en": "Huo Che Zhan"} in stations

    first = c.get("/jinhe/routes/2u/first").json
    assert first[0][0] == "7542"
    assert first[1][0] == "7527"
    assert first[-1][0] == "14495"
    assert len(first) == 28


def test_uc3():
    """查询锦城广场站停靠的所有线路。"""
    stations = c.get("/jinhe/stations/").json
    assert {s["id"] for s in stations if s["zh"] == "锦城广场"} == {
        "58290",
        "64355",
        "58289",
        "64356",
    }

    assert {n for n, _ in c.get("/jinhe/stations/58290/first").json} == {
        "K5u",
    }
    assert {n for n, _ in c.get("/jinhe/stations/64355/first").json} == {
        "N26d",
        "G33u",
        "17d",
    }
    assert {n for n, _ in c.get("/jinhe/stations/58289/first").json} == {
        "K5d",
    }
    assert {n for n, _ in c.get("/jinhe/stations/64356/first").json} == {
        "N26u",
        "G33d",
        "17u",
    }


def test_uc4():
    """查询某条线路从某站到某站，线路的运行方向、沿路站点和运行时长。"""
    # Route:10 is directional
    assert c.get("/jinhe/routes/").json["10"] == "1"

    # the expected direction is up
    stations = c.get("/jinhe/stations/").json
    p_id = {s["id"] for s in stations if s["zh"] == "大悦城"}
    q_id = {s["id"] for s in stations if s["zh"] == "小吃街"}
    u_first = c.get("/jinhe/routes/10u/first").json
    d_first = c.get("/jinhe/routes/10d/first").json
    u_p_arr = [i for i, x in enumerate(u_first) if x[0] in p_id]
    u_q_arr = [i for i, x in enumerate(u_first) if x[0] in q_id]
    d_p_arr = [i for i, x in enumerate(d_first) if x[0] in p_id]
    d_q_arr = [i for i, x in enumerate(d_first) if x[0] in q_id]
    assert len(u_p_arr) == 1
    assert len(u_q_arr) == 1
    assert len(d_p_arr) == 1
    assert len(d_q_arr) == 1
    u_p, u_q, d_p, d_q = u_p_arr[0], u_q_arr[0], d_p_arr[0], d_q_arr[0]
    assert u_p < u_q
    assert d_p > d_q

    # stations along the line
    assert [x[0] for x in u_first[u_p : u_q + 1]] == [
        "62753",
        "62765",
        "62737",
        "62729",
        "6354",
        "6363",
        "6377",
    ]

    # time
    assert u_first[u_q][1] - u_first[u_p][1] == 13
