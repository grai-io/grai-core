import uuid

import pytest

from lineage.graph import GraphQuery, Match
from lineage.graph_filter import filter_by_filter
from lineage.models import Filter


@pytest.mark.django_db
def test_incorrect_type():
    query = GraphQuery()

    filter = Filter(
        name=str(uuid.uuid4()),
        metadata=[
            {
                "type": "incorrect",
                "value": "test3",
            }
        ],
    )

    with pytest.raises(Exception) as e_info:
        filter_by_filter(filter, query)

    assert str(e_info.value) == "Unknown filter type: incorrect"


def test_empty():
    query = GraphQuery(Match("Table"))

    filter = Filter(
        name=str(uuid.uuid4()),
        metadata=[],
    )

    filter_by_filter(filter, query)

    assert len(query.clause[0].wheres) == 0
    assert query.parameters == {}


def test_table_name_equals():
    query = GraphQuery(Match("Table"))

    filter = Filter(
        name=str(uuid.uuid4()),
        metadata=[
            {
                "type": "table",
                "field": "name",
                "operator": "equals",
                "value": "test4",
            }
        ],
    )

    filter_by_filter(filter, query)

    assert len(query.clause[0].wheres) == 1
    assert query.clause[0].wheres[0].where == "toLower(table.name) = toLower('test4')"
    assert query.parameters == {}


def test_table_name_not_equals():
    query = GraphQuery(Match("Table"))

    filter = Filter(
        name=str(uuid.uuid4()),
        metadata=[
            {
                "type": "table",
                "field": "name",
                "operator": "not-equals",
                "value": "test2",
            }
        ],
    )

    filter_by_filter(filter, query)

    assert len(query.clause[0].wheres) == 1
    assert query.clause[0].wheres[0].where == "toLower(table.name) <> toLower('test2')"
    assert query.parameters == {}


def test_table_name_contains():
    query = GraphQuery(Match("Table"))

    filter = Filter(
        name=str(uuid.uuid4()),
        metadata=[
            {
                "type": "table",
                "field": "name",
                "operator": "contains",
                "value": "test3",
            }
        ],
    )

    filter_by_filter(filter, query)

    assert len(query.clause[0].wheres) == 1
    assert query.clause[0].wheres[0].where == "toLower(table.name) CONTAINS toLower('test3')"
    assert query.parameters == {}


def test_table_name_not_contains():
    query = GraphQuery(Match("Table"))

    filter = Filter(
        name=str(uuid.uuid4()),
        metadata=[
            {
                "type": "table",
                "field": "name",
                "operator": "not-contains",
                "value": "test3",
            }
        ],
    )

    filter_by_filter(filter, query)

    assert len(query.clause[0].wheres) == 1
    assert query.clause[0].wheres[0].where == "NOT toLower(table.name) CONTAINS toLower('test3')"
    assert query.parameters == {}


def test_table_name_starts_with():
    query = GraphQuery(Match("Table"))

    filter = Filter(
        name=str(uuid.uuid4()),
        metadata=[
            {
                "type": "table",
                "field": "name",
                "operator": "starts-with",
                "value": "test3",
            }
        ],
    )

    filter_by_filter(filter, query)

    assert len(query.clause[0].wheres) == 1
    assert query.clause[0].wheres[0].where == "toLower(table.name) STARTS WITH toLower('test3')"
    assert query.parameters == {}


def test_table_name_ends_with():
    query = GraphQuery(Match("Table"))

    filter = Filter(
        name=str(uuid.uuid4()),
        metadata=[
            {
                "type": "table",
                "field": "name",
                "operator": "ends-with",
                "value": "test3",
            }
        ],
    )

    filter_by_filter(filter, query)

    assert len(query.clause[0].wheres) == 1
    assert query.clause[0].wheres[0].where == "toLower(table.name) ENDS WITH toLower('test3')"
    assert query.parameters == {}


def test_no_ancestor():
    query = GraphQuery(Match("Table"))

    filter = Filter(
        name=str(uuid.uuid4()),
        metadata=[
            {
                "type": "no-ancestor",
                "field": "tag",
                "operator": "contains",
                "value": "test4",
            }
        ],
    )

    filter_by_filter(filter, query)

    assert len(query.clause[0].wheres) == 0
    assert query.parameters == {}


def test_no_descendant():
    query = GraphQuery(Match("Table"))

    filter = Filter(
        name=str(uuid.uuid4()),
        metadata=[
            {
                "type": "no-descendant",
                "field": "tag",
                "operator": "contains",
                "value": "test4",
            }
        ],
    )

    filter_by_filter(filter, query)

    assert len(query.clause[0].wheres) == 0
    assert query.parameters == {}
