from fastapi import Request
from fastapi.responses import JSONResponse

from app.i18n.manager import i18n


def localized_error_response(
    request: Request,
    status_code: int,
    key: str,
):
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": i18n.translate(key),
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
