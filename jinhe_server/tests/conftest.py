from time import sleep

import pytest


@pytest.fixture(scope="session")
def setup():
    """Wait for database."""
    sleep(3)
