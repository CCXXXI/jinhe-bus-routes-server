from flask import Blueprint

from . import r

bp = Blueprint("meta", __name__, url_prefix="/meta")


@bp.route("/version")
def version():
    """The Git commit ID of the data."""
    return r.get("version")
