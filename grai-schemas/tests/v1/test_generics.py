import pytest
from grai_schemas.v1.generics import (
    CPP,
    PHP,
    SAS,
    SQL,
    C,
    Code,
    CSharp,
    Go,
    Haskell,
    Java,
    JavaScript,
    Julia,
    Kotlin,
    Matlab,
    Perl,
    ProgrammingLanguage,
    Python,
    R,
    Rust,
    Scala,
    Swift,
    TypeScript,
    UnknownLanguage,
)

languages = [
    ("Python", Python),
    ("R", R),
    ("SQL", SQL),
    ("Unknown", UnknownLanguage),
    ("C", C),
    ("C#", CSharp),
    ("C++", CPP),
    ("Java", Java),
    ("Scala", Scala),
    ("Go", Go),
    ("JavaScript", JavaScript),
    ("TypeScript", TypeScript),
    ("Matlab", Matlab),
    ("Swift", Swift),
    ("Julia", Julia),
    ("SAS", SAS),
    ("Rust", Rust),
    ("Perl", Perl),
    ("Haskell", Haskell),
    ("PHP", PHP),
    ("Kotlin", Kotlin),
]


class TestCode:
    @pytest.mark.parametrize("language_name, expected", languages)
    def test_language_name_from_str(self, language_name, expected):
        assert Code(language=language_name).language == expected()

    @pytest.mark.parametrize("language_name, expected", languages)
    def test_language_name(self, language_name, expected):
        assert Code(language=expected()).language == expected()

    @pytest.mark.parametrize("language_name, expected", languages)
    def test_language_name_from_dict(self, language_name, expected):
        assert Code(language={"language_name": language_name}).language == expected()

    @pytest.mark.parametrize("language_name, expected", languages)
    def test_all_languages_are_programming_languages(self, language_name, expected):
        assert isinstance(Code(language={"language_name": language_name}).language, ProgrammingLanguage)
