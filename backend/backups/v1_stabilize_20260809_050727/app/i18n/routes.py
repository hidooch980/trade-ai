from fastapi import APIRouter, Request

from app.i18n.manager import i18n, SUPPORTED_LANGUAGES

router = APIRouter(prefix="/i18n", tags=["i18n"])


@router.get("/languages")
async def languages():
    return {
        "default": "en",
        "supported": list(SUPPORTED_LANGUAGES),
    }


@router.get("/current")
async def current_language(request: Request):
    language = request.query_params.get("lang")

    if language:
        language = i18n.set_language(language)
    else:
        language = request.headers.get("Accept-Language", "en")

        if language:
            language = i18n.set_language(language.split(",", 1)[0])

    return {
        "language": language,
        "supported": list(SUPPORTED_LANGUAGES),
    }
