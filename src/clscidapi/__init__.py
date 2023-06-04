"""A FastAPI app that allows HTTP-based lookup of new ID by classic ID."""

__version__ = "0.0.1"

import json
import os

from . import config


CONF = config.Config()
CLASSIC_URL = "http://classic.avalanche.state.co.us/caic/obs/obs_report.php?obs_id={id}"
NEW_URL = "https://avalanche.state.co.us/observations/field-report/{id}"

try:
    with open(
        os.path.expandvars(os.path.expanduser(CONF.clsc_ids_json)),
        "r",
        encoding="utf-8",
    ) as id_fd:
        CLASSIC_IDS = json.load(id_fd)
except Exception as err:
    raise SystemExit(
        f"Unable to load Classic IDs file from {CONF.clsc_ids_json}"
    ) from err


def find_id(classic_id: str) -> str | None:
    """Find a new ID based on the given classic ID."""

    if classic_id in CLASSIC_IDS:
        return CLASSIC_IDS[classic_id]
    return None
