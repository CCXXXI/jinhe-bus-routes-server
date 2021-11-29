from src import app


def test_version():
    """The Git commit ID is a 40 digits long SHA-1 hash."""
    assert len(app.version()) == 40


def test_route():
    """UC-1: 查询某条线路的基本信息"""
    assert app.route("30") == {
        "direction": "燎原-北路湾公交站",
        "oneway": "约49分",
        "directional": "1",
        "kilometer": "12.0",
        "runtime": "6:30-22:30",
        "interval": "8",
        "type": "干线",
    }
