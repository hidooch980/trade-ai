import json
from contextvars import ContextVar
from pathlib import Path
from typing import Any

SUPPORTED_LANGUAGES = ("fa", "en", "de", "ar")
DEFAULT_LANGUAGE = "en"

_LOCALES_DIR = Path(__file__).resolve().parent / "locales"

_current_language: ContextVar[str] = ContextVar(
    "current_language",
    default=DEFAULT_LANGUAGE,
)


def normalize_language(language: str | None) -> str:
    if not language:
        return DEFAULT_LANGUAGE

    language = language.lower().strip()

    if "-" in language:
        language = language.split("-", 1)[0]

    if "_" in language:
        language = language.split("_", 1)[0]

    if language in SUPPORTED_LANGUAGES:
        return language

    return DEFAULT_LANGUAGE


def _load_translations() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}

    for language in SUPPORTED_LANGUAGES:
        path = _LOCALES_DIR / f"{language}.json"

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise RuntimeError(f"INVALID_LOCALE_FILE:{language}")

        result[language] = data

    return result


TRANSLATIONS = _load_translations()


class I18nManager:
    def set_language(self, language: str | None) -> str:
        normalized = normalize_language(language)
        _current_language.set(normalized)
        return normalized

    def get_language(self) -> str:
        return _current_language.get()

    def translate(
        self,
        key: str,
        language: str | None = None,
        **kwargs: Any,
    ) -> str:
        lang = (
            normalize_language(language)
            if language
            else self.get_language()
        )

        text = TRANSLATIONS.get(lang, {}).get(key)

        if text is None:
            text = TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key)

        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError):
                pass

        return text

    def languages(self) -> list[str]:
        return list(SUPPORTED_LANGUAGES)


i18n = I18nManager()
