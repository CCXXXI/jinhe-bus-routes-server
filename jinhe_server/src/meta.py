from flask import Blueprint

from . import cached, r

bp = Blueprint("meta", __name__, url_prefix="/meta")


@bp.route("/version")
@cached()
def version():
    """The Git commit ID of the data."""
    return r.get("version")
