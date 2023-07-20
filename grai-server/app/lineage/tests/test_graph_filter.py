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


def test_table_name_not_equals():
    match2 = Match("Table2")
    query2 = GraphQuery(match2)

    filter2 = Filter(
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

    filter_by_filter(filter2, query2)

    assert len(query2.clause[0].wheres) == 1
    assert query2.clause[0].wheres[0].where == "toLower(table.name) <> toLower('test2')"
    assert query2.parameters == {}


def test_table_name_equals():
    match3 = Match("Table")
    query3 = GraphQuery(match3)

    assert len(query3.clause[0].wheres) == 0

    filter3 = Filter(
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

    filter_by_filter(filter3, query3)

    assert len(query3.clause[0].wheres) == 1
    assert query3.clause[0].wheres[0].where == "toLower(table.name) = toLower('test4')"
    assert query3.parameters == {}
