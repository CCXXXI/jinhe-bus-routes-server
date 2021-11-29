from src.app import version


def test_version():
    """The Git commit ID is a 40 digits long SHA-1 hash."""
    assert len(version()) == 40
