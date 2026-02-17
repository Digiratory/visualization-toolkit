"""Test languages from config."""

from visualization_toolkit.localization import en, ru


def test_languages_same_keys():
    """
    Test that both languages have the same keys.
    """
    ru_keys = set(ru.TRANSLATIONS.keys())
    en_keys = set(en.TRANSLATIONS.keys())

    only_in_ru = ru_keys - en_keys
    only_in_en = en_keys - ru_keys

    assert not only_in_ru, f"Ru only keys: {only_in_ru}"
    assert not only_in_en, f"En only keys: {only_in_en}"
