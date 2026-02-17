"""Global configuration for the project."""

from typing import Any, Dict

from .localization import en, ru


class LibraryConfig:
    """Глобальная конфигурация библиотеки"""

    _instance = None
    _translations = {
        "ru": ru.TRANSLATIONS,
        "en": en.TRANSLATIONS,
    }
    _current_language = "en"
    _custom_translations: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def set_language(cls, language: str) -> None:
        """
        Set the current language for the library.

        Parameters:
           language (str): The language code to set. Supported languages are 'ru' and 'en'.
        Returns:
           None
        """
        if language not in cls._translations:
            available = list(cls._translations.keys())
            raise ValueError(
                f"Language '{language}' not supported. Available: {available}"
            )
        cls._current_language = language

    @classmethod
    def get_language(cls) -> str:
        """
        Get the current language for the library.

        Returns:
          str: The current language code.
        """
        return cls._current_language

    @classmethod
    def get_text(cls, key: str, **kwargs) -> str:
        """
        Get the translated text for a given key.

        Parameters:
           key (str): The key to look up in the current language.
        Returns:
          str: The translated text.
        """
        if key in cls._custom_translations:
            template = cls._custom_translations[key]
        else:
            translations = cls._translations.get(cls._current_language, {})
            template = translations.get(key, key)

        if kwargs:
            return template.format(**kwargs)
        return template


config = LibraryConfig()


def set_language(language: str) -> None:
    """Setting the interface language

    Parameters:
        language (str): Language code

    Usage example:
    >>> from visualization_toolkit.config import set_language
    >>> set_language("ru")
    """
    config.set_language(language)


def get_text(key: str) -> str:
    """
    Get the translated text for a given key.

    Parameters:
        key (str): The key to look up in the current language.
    Returns:
        str: The translated text.
    """
    return config.get_text(key)
