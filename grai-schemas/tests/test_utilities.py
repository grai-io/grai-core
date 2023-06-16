import pytest
from grai_schemas.utilities import merge
from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.metadata.metadata import GraiMalformedNodeMetadataV1, MetadataV1
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

    def test_merge_valid_node_metadata_into_malformed(self):
        a = GraiMalformedNodeMetadataV1()
        b = MetadataV1(grai={"node_type": "Generic"})

        assert merge(a, b) == MetadataV1(grai={"node_type": "Generic"})

    def test_merge_valid_edge_metadata_into_malformed(self):
        a = GraiMalformedNodeMetadataV1()
        b = MetadataV1(grai={"edge_type": "Generic"})

        assert merge(a, b) == MetadataV1(grai={"edge_type": "Generic"})

    @pytest.mark.xfail
    def test_marge_malformed_node_metadata_into_valid(self):
        a = MetadataV1(grai={"node_type": "Generic"})
        b = GraiMalformedNodeMetadataV1()

        merge(a, b)

    @pytest.mark.xfail
    def test_marge_malformed_edge_metadata_into_valid(self):
        a = MetadataV1(grai={"edge_type": "Generic"})
        b = GraiMalformedNodeMetadataV1()

        merge(a, b)

    def test_merge_full_node_into_malformed_node(self):
        base_node = {"name": "test", "namespace": "test", "data_source": "test", "metadata": {}}

        a = NodeV1.from_spec(base_node)
        a.spec.metadata = GraiMalformedNodeMetadataV1()
        b = NodeV1.from_spec(base_node)
        assert merge(a, b) == b

    def test_merge_full_edge_into_malformed_node(self):
        base_edge = {
            "name": "test",
            "namespace": "test",
            "data_source": "test",
            "source": {"name": "test", "namespace": "test"},
            "destination": {"name": "test2", "namespace": "test"},
            "metadata": {},
        }

        a = EdgeV1.from_spec(base_edge)
        a.spec.metadata = GraiMalformedNodeMetadataV1()
        b = EdgeV1.from_spec(base_edge)
        assert merge(a, b) == b
