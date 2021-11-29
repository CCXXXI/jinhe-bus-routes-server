from time import sleep

from src import app


def setup_module():
    """Wait for database."""
    sleep(3)


def test_version():
    """The Git commit ID is a 40 digits long SHA-1 hash."""
    assert len(app.version()) == 40


def test_routes():
    """UC-1"""
    assert app.routes()["30"] == "1"
    assert app.routes_name("30") == {
        "direction": "燎原-北路湾公交站",
        "oneway": "约49分",
        "kilometer": "12.0",
        "runtime": "6:30-22:30",
        "interval": "8",
        "type": "干线",
    }
