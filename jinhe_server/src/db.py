from os import getenv

from flask import g
from redis import Redis
from redisgraph import Graph


def get_db():
    """Get the global Redis instance and the Graph instance."""
    if "db" not in g:
        g.db = Redis(host=getenv("JINHE_DATA_HOST", "localhost"), decode_responses=True)
    return g.db, Graph("g", g.db)
