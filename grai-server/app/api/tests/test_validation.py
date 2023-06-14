import pytest

from api.validation import validate_no_slash


def test_validate_no_slash():
    validate_no_slash("abc", "field")


def test_validate_no_slash_fail():
    with pytest.raises(Exception) as e_info:
        validate_no_slash("abc/def", "field")

    assert str(e_info.value) == "field contains forward slash"
