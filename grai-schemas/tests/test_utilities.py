from grai_schemas.utilities import merge
from pydantic import BaseModel


class TestMerge:
    """ """

    def test_merge_pydantic(self):
        """test that two BaseModels can be successfully merged into a dictionary"""

        class Model(BaseModel):
            """ """

            a: int
            b: int

        a = Model(a=1, b=2)
        b = Model(a=3, b=4)

        assert merge(a, b) == {"a": 3, "b": 4}

    def test_merge_pydantic_to_dict(self):
        """test that a BaseModel can be successfully merged into a dictionary"""

        class Model(BaseModel):
            """ """

            a: int
            b: int

        a = Model(a=1, b=2)
        b = {"a": 3, "b": 4}

        assert merge(a, b) == {"a": 3, "b": 4}

    def test_merge_dict_to_pydantic(self):
        """test that a dictionary can be successfully merged into a BaseModel"""

        class Model(BaseModel):
            """ """

            a: int
            b: int

        a = {"a": 1, "b": 2}
        b = Model(a=3, b=4)

        assert merge(a, b) == {"a": 3, "b": 4}

    def test_merge_lists(self):
        """test that two lists can be successfully merged"""
        a = [1, 2, 3]
        b = [4, 5, 6]

        assert merge(a, b) == [1, 2, 3, 4, 5, 6]

    def test_merge_to_missing_key(self):
        """test that a key can be merged into a missing key"""
        a = {}
        b = {"a": 1}

        assert merge(a, b) == {"a": 1}

    def test_merge_from_missing_key(self):
        """test that a key can be merged from a missing key"""
        a = {"a": 1}
        b = {}

        assert merge(a, b) == {"a": 1}

    def test_merge_to_missing_index(self):
        """test that an index can be merged into a missing index"""
        a = []
        b = [1]

        assert merge(a, b) == [1]

    def test_merge_from_missing_index(self):
        """test that an index can be merged from a missing index"""
        a = [1]
        b = []

        assert merge(a, b) == [1]

    def test_merge_tuples(self):
        """test that two tuples can be successfully merged"""
        a = (1, 2, 3)
        b = (4, 5, 6)

        assert merge(a, b) == (1, 2, 3, 4, 5, 6)

    def test_merge_sets(self):
        """test that two sets can be successfully merged"""
        a = {1, 2, 3}
        b = {4, 5, 6}

        assert merge(a, b) == {1, 2, 3, 4, 5, 6}

    def test_merge_set_with_overlap(self):
        """test that two sets with overlap can be successfully merged"""
        a = {1, 2, 3}
        b = {3, 4, 5}

        assert merge(a, b) == {1, 2, 3, 4, 5}

    def test_merge_to_missing_value(self):
        """test that a value can be merged into a missing value"""
        a = None
        b = 1

        assert merge(a, b) == 1

    def test_merge_from_missing_value(self):
        """test that a value can be merged from a missing value"""
        a = 1
        b = None

        assert merge(a, b) == 1

    def test_atomic_merge(self):
        """test that two atomic values can be merged"""
        a = 1
        b = 2

        assert merge(a, b) == 2
