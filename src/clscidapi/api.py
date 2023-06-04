"""A FastAPI app that allows HTTP-based lookup of new ID by classic ID."""

import urllib.parse

import fastapi
import starlette.responses
import starlette.status

from . import CLASSIC_URL, CONF, find_id, models, NEW_URL, __version__

app = fastapi.FastAPI(
    title=f"CAIC Classic ID to New ID Converter - v{__version__}",
    version=__version__,
    debug=CONF.api_debug,
)


def return_err(
    msg: str,
    response: starlette.responses.Response,
    err_code: int = starlette.status.HTTP_400_BAD_REQUEST,
) -> models.ApiResponse:
    """Return an error response."""

    response.status_code = err_code
    return models.ApiResponse(status=models.Statuses.ERROR, data="", msg=msg)


@app.get("/")
def root() -> models.ApiResponse:
    """Return a simple object when the root URL is hit."""

    return {
        "status": models.Statuses.SUCCESS,
        "msg": "Use the '/clscid-lookup' endpoint!",
        "data": "",
    }


@app.get("/clscid-lookup")
async def clscid_lookup(
    response: starlette.responses.Response,
    query: int | str | None = fastapi.Query(default=None, alias="q"),
    redirect: bool = fastapi.Query(default=False, alias="r"),
    classic: bool = fastapi.Query(default=False, alias="c"),
    url: bool = fastapi.Query(default=True, alias="u"),
) -> models.ApiResponse:
    """Lookup a CAIC Classic ID and return the new CAIC ID.

    This endpoint can optionally return an HTTP redirect to the corresponding
    new CAIC field report page. Otherwise a JSON object containing the URL
    is returned.

    The input classic ID (``query``) can either be the raw ID, or an old classic
    URL that has the ID in the URL as the ``obs_id`` parameter.

    Parameters
    ----------
    response : starlette.responses.Response
        The object of the eventual HTTP response.
    query : int | str | None, optional
        The ID (or URL with ID) to query for, by default None.
    redirect : bool, optional
        Whether this endpoint will perform an HTTP redirect. By default False.
    url : bool, optional
        Whether to return a full URL of the generated Field Report or to return
        the raw ID. Doesn't impact redirects. By default True.
    classic : bool, optional
        Whether this endpoint returns a working classic URL instead of the new
        Field Report URL. This also affects this endpoint's redirects.
        By default False.

    Returns
    -------
    models.ApiResponse
        The response object. This is not returned when ``redirect`` is ``True``. Instead a
        ``starlette.responses.RedirectResponse`` is returned. Contains the following keys::

            data
            status
            msg
        
    """

    if isinstance(query, str):
        url = urllib.parse.urlparse(query)
        if url.query:
            queries = urllib.parse.parse_qs(url.query)
            if "obs_id" in queries:
                _id = int(queries["obs_id"][0])
    elif isinstance(query, int):
        _id = query
    else:
        _id = None

    if _id and _id > CONF.max_classic_ids:
        return return_err("The supplied ID was too large.", response)
    elif _id is None:
        return return_err("Must specify a value to query.", response)
    else:
        new_id = find_id(str(_id))

    if new_id is None:
        return return_err(
            "Could not find a new ID for the given classic ID",
            response,
            err_code=starlette.status.HTTP_404_NOT_FOUND,
        )

    if classic:
        ret_url = CLASSIC_URL.format(id=_id)
    else:
        ret_url = NEW_URL.format(id=new_id)

    if redirect:
        return starlette.responses.RedirectResponse(url=ret_url)

    if url:
        data = ret_url
    else:
        data = new_id

    return {
        "data": data,
        "status": models.Statuses.SUCCESS,
        "msg": "Found a corresponding new ID!",
    }
