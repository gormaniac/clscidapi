"""Models for the API."""

import enum
import pydantic


class Statuses(enum.Enum):
    """Possible values for a response status."""

    SUCCESS: str = "success"
    ERROR: str = "error"


class ApiResponse(pydantic.BaseModel):
    """A response from the API."""

    status: Statuses
    data: str
    msg: str
