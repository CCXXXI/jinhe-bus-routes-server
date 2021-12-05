from os import getenv

from flask import g
from redis import Redis
from redisgraph import Graph


def get_redis_host():
    """Get the host of the Redis database."""
    return getenv("JINHE_DATA_HOST", "localhost")


def get_db():
    """Get the global Redis instance and the Graph instance."""
    if "db" not in g:
        g.db = Redis(host=get_redis_host(), decode_responses=True)
    return g.db, Graph("g", g.db)
