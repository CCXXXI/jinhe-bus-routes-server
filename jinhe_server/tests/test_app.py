from bisect import bisect_left

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


def test_uc5():
    """查询某两个站台之间的最短路径。"""
    sp_id = c.get("/jinhe/paths/shortest/16115/14768").json["s"]
    assert sp_id == ["16115", "59548", "5181", "5197", "5168", "14768"]


def test_uc6():
    """查询某两个站台间是否存在直达线路。"""
    stations = c.get("/jinhe/stations/").json
    p_id = {s["id"] for s in stations if s["zh"] == "荷花池"}
    q_id = {s["id"] for s in stations if s["zh"] == "环球中心(始发站)"}

    p = {n for i in p_id for n, _ in c.get(f"/jinhe/stations/{i}/first").json}
    q = {n for i in q_id for n, _ in c.get(f"/jinhe/stations/{i}/first").json}

    assert p & q == {"N12u", "N12d"}


def test_uc7():
    """查询某条线路某个方向的全部班次信息。"""
    first = c.get("/jinhe/routes/239u/first").json
    assert first[0][1] == 7 * 60
    assert first[1][1] == 7 * 60 + 2
    assert first[2][1] == 7 * 60 + 4
    assert first[3][1] == 7 * 60 + 6
    assert first[4][1] == 7 * 60 + 8
    assert first[5][1] == 7 * 60 + 10
    assert first[6][1] == 7 * 60 + 12
    assert first[7][1] == 7 * 60 + 14

    steps = c.get("/jinhe/routes/239u/steps").json
    assert steps[0] == 0
    assert steps[1] == 6


def test_uc8():
    """查询某个时刻某个站台某个时段内即将停靠的线路。"""
    first = c.get("/jinhe/stations/16147/first").json
    assert {x[0] for x in first} >= {"53d", "70u", "101"}

    now, limit = 8 * 60 + 37, 5
    assert {
        n: time
        for n, f in first
        if (
            time := (steps := c.get(f"/jinhe/routes/{n}/steps").json)[
                bisect_left(steps, now - f)
            ]
            - (now - f)
        )
        <= limit
    } == {"101": 0, "174d": 3, "53d": 1, "70u": 5}


def test_uc9():
    """查询某个时刻某个站台线路最近的3趟班次信息。"""
    first = c.get("/jinhe/stations/59760/first").json
    assert {x[0] for x in first} >= {"106u", "82u", "99u"}

    now = 10 * 60 + 32
    res = {}
    for n, f in first:
        res[n] = []
        for x in (steps := c.get(f"/jinhe/routes/{n}/steps").json)[
            (start := bisect_left(steps, now - f)) : start + 3
        ]:
            res[n].append(x - (now - f))
    assert dict(filter(lambda x: x[1], res.items())) == {
        "106u": [7, 15, 23],
        "82u": [1, 7, 13],
        "99u": [4, 10, 16],
    }


def test_uc10():
    """统计停靠路线最多的站点并排序。"""
    r = c.get("/jinhe/stats/stations/routes").json

    assert r[0][0] == "818"
    assert r[1][0] == "24645"
    assert r[2][0] == "24646"

    assert r[0][1] == 13
    assert r[1][1] == 11
    assert r[2][1] == 11

    assert set(r[0][2]) > {"N12d", "N11d", "G38u", "G37d", "G28d", "G22d", "759u"}
    assert set(r[1][2]) > {"N31u", "G90u", "G41", "736d", "735d", "727Ad", "727d"}
    assert set(r[2][2]) > {"N31d", "G90d", "G41", "736u", "735u", "727Au", "727u"}


def test_uc11():
    """统计特殊站台。"""
    stations = {s["zh"] for s in c.get("/jinhe/stations/").json}

    assert sum(s.startswith("地铁") for s in stations) == 20
    assert sum(s.endswith("(始发站)") for s in stations) == 59
    assert sum(s.endswith("(终点站)") for s in stations) == 59


def test_uc12():
    """分组统计路线类型。"""
    r = c.get("/jinhe/stats/routes/types").json
    assert r == {
        "干线": 36,
        "高峰线": 16,
        "夜班线": 11,
        "城乡线": 8,
        "支线": 8,
        "快速公交": 7,
        "驳接线": 5,
        "社区线": 2,
    }


def test_uc13():
    """查询两条线路重复的站点名。"""
    u = {f[0] for f in c.get("/jinhe/routes/15u/first").json}
    v = {f[0] for f in c.get("/jinhe/routes/30d/first").json}
    assert u & v == {"17848", "17824", "17809"}


def test_uc14():
    """查询换乘线路。"""
    stations = {s["id"]: s["zh"] for s in c.get("/jinhe/stations/").json}
    assert {
        stations[s[0]]: routes
        for s in c.get("/jinhe/routes/261u/first").json
        if (
            routes := {x[0] for x in c.get(f"/jinhe/stations/{s[0]}/first").json}
            - {"261u"}
        )
    } == {
        "凤溪大道中": {"70d", "74d", "322u", "727u", "735u", "736u", "G41", "N31d"},
        "培风路北": {"30d", "208u"},
        "双水村": {"15d", "16d", "N20u"},
        "医学院": {"30d", "208u"},
        "花博路": {"70d", "74d", "736u", "G41"},
        "凤溪大道和桥": {
            "70d",
            "74d",
            "322u",
            "727u",
            "727Au",
            "735u",
            "736u",
            "G41",
            "G90d",
            "N31d",
        },
        "星空大道武科路口": {"15d", "16d", "G41", "N20u"},
        "天府家园": {"15d", "16d", "N20u"},
        "花博路口": {"70d", "74d", "736u", "G41"},
        "星空大道南": {"16d", "30d", "735u", "N20u"},
    }


def test_uc15():
    """根据连接两个相邻站台之间线路数量排序两个相邻站台。"""
    r = c.get("/jinhe/stats/stations/links").json
    assert ["凤溪大道中", "凤溪大道和桥", 9] in r
    assert ["凤溪大道和桥", "凤溪大道中", 9] in r
    assert ["科北路口", "北门立交南", 8] in r
    assert ["凤溪大道和桥", "河野", 8] in r


def test_uc16():
    """根据站点数量对线路进行排序。"""
    r = c.get("/jinhe/stats/routes/stations").json
    assert ["736u", 47] in r
    assert ["736d", 46] in r
    assert ["735d", 44] in r
    assert ["735u", 44] in r


def test_uc17():
    """根据运行时间对线路进行排序。"""
    r = c.get("/jinhe/stats/routes/time").json
    assert ["736u", 90] in r
    assert ["736d", 90] in r
    assert ["735d", 86] in r
    assert ["735u", 86] in r
