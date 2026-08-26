from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse

from app.i18n.manager import i18n


def _default_phrase(status_code: int) -> str:
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return ""


def localized_error_response(
    request: Request,
    status_code: int,
    key: str,
    detail=None,
):
    """
    Localized error body.

    A handler that took the trouble to say *what* went wrong keeps its own
    message; a bare `raise HTTPException(404)` still gets the translated
    generic text. `error` carries the stable key either way, so a client can
    branch on the class of failure without parsing prose.
    """
    generic = i18n.translate(key)

    if (
        isinstance(detail, str)
        and detail.strip()
        and detail.strip() != _default_phrase(status_code)
    ):
        body_detail = detail
    elif detail is not None and not isinstance(detail, str):
        # Validation errors arrive as a list of field problems.
        body_detail = detail
    else:
        body_detail = generic

    return JSONResponse(
        status_code=status_code,
        content={
            "detail": body_detail,
            "error": key,
            "message": generic,
            "status_code": status_code,
            "language": i18n.get_language(),
        },
    )


async def http_exception_handler(request: Request, exc):
    language = request.query_params.get("lang")

    if not language:
        language = request.headers.get("Accept-Language")

    i18n.set_language(language)

    if exc.status_code == 401:
        key = "error.unauthorized"
    elif exc.status_code == 403:
        key = "error.forbidden"
    elif exc.status_code == 404:
        key = "error.not_found"
    elif exc.status_code == 405:
        key = "error.method_not_allowed"
    elif exc.status_code == 422:
        key = "error.validation"
    else:
        key = "error.http"

    return localized_error_response(
        request,
        exc.status_code,
        key,
        detail=getattr(exc, "detail", None),
    )


async def general_exception_handler(request: Request, exc):
    language = request.query_params.get("lang")

    if not language:
        language = request.headers.get("Accept-Language")

    i18n.set_language(language)

    return localized_error_response(
        request,
        500,
        "error.internal",
    )


async def validation_exception_handler(request: Request, exc):
    """
    FastAPI raises RequestValidationError, not HTTPException, so a 422 never
    reached the handler above and came back in a different shape from every
    other error. Same envelope here, with `detail` as something a UI can
    print and `errors` keeping the full per-field list.
    """
    language = request.query_params.get("lang")

    if not language:
        language = request.headers.get("Accept-Language")

    i18n.set_language(language)

    problems = exc.errors() if hasattr(exc, "errors") else []

    fields = []
    for problem in problems:
        location = [str(part) for part in problem.get("loc", ()) if part != "body"]
        if location:
            fields.append(".".join(location))

    generic = i18n.translate("error.validation")

    return JSONResponse(
        status_code=422,
        content={
            "detail": f"{generic}: {', '.join(fields)}" if fields else generic,
            "error": "error.validation",
            "message": generic,
            "status_code": 422,
            "language": i18n.get_language(),
            "fields": fields,
        },
    )
