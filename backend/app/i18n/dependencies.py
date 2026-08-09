from fastapi import Request

from app.i18n.manager import i18n, normalize_language


def get_request_language(request: Request) -> str:
    query_language = request.query_params.get("lang")

    if query_language:
        return i18n.set_language(query_language)

    header = request.headers.get("Accept-Language")

    if header:
        first = header.split(",", 1)[0].split(";", 1)[0].strip()
        return i18n.set_language(normalize_language(first))

    return i18n.set_language(None)
