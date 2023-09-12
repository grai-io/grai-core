import pytest

from lineage.graph import GraphQuery, Match, Where


class TestWhere:
    def test_init(self):
        where = Where(where="a = b")

        assert where.where == "a = b"
        assert where.parameters == {}
        assert str(where) == "a = b"

    def test_init_parameters(self):
        where = Where(where="a = b", parameters={"a": "b"})

        assert where.where == "a = b"
        assert where.parameters == {"a": "b"}
        assert str(where) == "a = b"


class TestMatch:
    def test_init(self):
        match = Match(match="(a)")

        assert match.match == "(a)"
        assert match.wheres == []
        assert match.parameters == {}
        assert str(match) == "MATCH (a)"
        assert match.get_parameters() == {}

    def test_init_optional(self):
        match = Match(match="(a)", optional=True)

        assert match.match == "(a)"
        assert match.wheres == []
        assert match.parameters == {}
        assert str(match) == "OPTIONAL MATCH (a)"
        assert match.get_parameters() == {}

    def test_init_where(self):
        match = Match(match="(a)", where="a = b")

        assert match.match == "(a)"
        assert str(match.wheres[0]) == "a = b"
        assert match.parameters == {}
        assert str(match) == "MATCH (a) WHERE a = b"
        assert match.get_parameters() == {}

    def test_init_where_class(self):
        where = Where(where="a = b")
        match = Match(match="(a)", where=where)

        assert match.match == "(a)"
        assert match.wheres[0] == where
        assert match.parameters == {}
        assert str(match) == "MATCH (a) WHERE a = b"
        assert match.get_parameters() == {}

    def test_init_where_class_parameters(self):
        where = Where(where="a = b", parameters={"a": "b"})
        match = Match(match="(a)", where=where)

        assert match.match == "(a)"
        assert match.wheres[0] == where
        assert match.parameters == {}
        assert str(match) == "MATCH (a) WHERE a = b"
        assert match.get_parameters() == {"a": "b"}

    def test_init_where_list(self):
        where = Where(where="a = b")
        where2 = Where(where="b = c")
        match = Match(match="(a)", where=[where, where2])

        assert match.match == "(a)"
        assert match.wheres[0] == where
        assert match.wheres[1] == where2
        assert match.parameters == {}
        assert str(match) == "MATCH (a) WHERE a = b AND b = c"
        assert match.get_parameters() == {}

    def test_init_parameters(self):
        match = Match(match="(a)", parameters={"a": "b"})

        assert match.match == "(a)"
        assert str(match) == "MATCH (a)"
        assert match.parameters == {"a": "b"}
        assert match.get_parameters() == {"a": "b"}

    def test_where(self):
        match = Match(match="(a)").where("a = b")

        assert match.match == "(a)"
        assert str(match.wheres[0]) == "a = b"
        assert match.parameters == {}
        assert str(match) == "MATCH (a) WHERE a = b"
        assert match.get_parameters() == {}

    def test_where_class(self):
        where = Where(where="a = b")
        match = Match(match="(a)", where=[]).where(where)

        assert match.match == "(a)"
        assert match.wheres[0] == where
        assert match.parameters == {}
        assert str(match) == "MATCH (a) WHERE a = b"
        assert match.get_parameters() == {}

    def test_where_list(self):
        where = Where(where="a = b")
        where2 = Where(where="b = c")
        match = Match(match="(a)", where=[]).where([where, where2])

        assert match.match == "(a)"
        assert match.wheres[0] == where
        assert match.parameters == {}
        assert str(match) == "MATCH (a) WHERE a = b AND b = c"
        assert match.get_parameters() == {}


class TestGraphQuery:
    def test_init(self):
        query = GraphQuery()

        assert query.clause == []
        assert query.parameters == {}
        assert str(query) == ""
        assert query.get_parameters() == {}

    def test_init_match(self):
        match = Match(match="(a)", where=[])
        query = GraphQuery(clause=match)

        assert query.clause[0].match == "(a)"
        assert query.parameters == {}
        assert str(query) == "MATCH (a)"
        assert query.get_parameters() == {}

    def test_init_match_list(self):
        match = Match(match="(a)", where=[])
        query = GraphQuery(clause=[match])

        assert query.clause[0].match == "(a)"
        assert query.parameters == {}
        assert str(query) == "MATCH (a)"
        assert query.get_parameters() == {}

    def test_init_parameters(self):
        query = GraphQuery(parameters={"a": "b"})

        assert query.clause == []
        assert query.parameters == {"a": "b"}
        assert str(query) == ""
        assert query.get_parameters() == {"a": "b"}

    def test_match(self):
        query = GraphQuery().match("(a)", where=[])

        assert query.clause[0].match == "(a)"
        assert query.parameters == {}
        assert str(query) == "MATCH (a)"
        assert query.get_parameters() == {}

    def test_match_class(self):
        match = Match(match="(a)", where=[])
        query = GraphQuery(clause=[]).match(match)

        assert query.clause[0] == match
        assert query.parameters == {}
        assert str(query) == "MATCH (a)"
        assert query.get_parameters() == {}

    def test_match_list(self):
        match = Match(match="(a)", where=[])
        match2 = Match(match="(b)", where=[])
        query = GraphQuery(clause=[], parameters={}).match([match, match2])

        assert query.clause[0].match == "(a)"
        assert query.clause[1].match == "(b)"
        assert query.parameters == {}
        assert str(query) == "MATCH (a) MATCH (b)"
        assert query.get_parameters() == {}

    def test_where(self):
        query = GraphQuery(Match("(a)", where=[])).where("a = b")

        assert query.clause[0].wheres[0].where == "a = b"
        assert query.parameters == {}
        assert str(query) == "MATCH (a) WHERE a = b"
        assert query.get_parameters() == {}

    def test_where_class(self):
        where = Where(where="a = b")
        query = GraphQuery(Match("(a)", where=[])).where(where)

        assert query.clause[0].wheres[0] == where
        assert query.parameters == {}
        assert str(query) == "MATCH (a) WHERE a = b"
        assert query.get_parameters() == {}

    def test_where_list(self):
        where = Where(where="a = b")
        where2 = Where(where="b = c")
        query = GraphQuery(Match("(a)", where=[])).where([where, where2])

        assert query.clause[0].wheres[0] == where
        assert query.clause[0].wheres[1] == where2
        assert query.parameters == {}
        assert str(query) == "MATCH (a) WHERE a = b AND b = c"
        assert query.get_parameters() == {}

    def test_where_no_match(self):
        with pytest.raises(Exception) as e_info:
            query = GraphQuery(clause="abc").where("a = b")

        assert str(e_info.value) == "Cannot add where clause to non-match clause"

    def test_add(self):
        query = GraphQuery(clause="(a)").add("abc")

        assert str(query.clause[1]) == "abc"
        assert query.parameters == {}
        assert str(query) == "(a) abc"

    def test_add_class(self):
        query2 = GraphQuery(clause="(b)")

        query = GraphQuery(clause="(a)").add(query2)

        assert query.parameters == {}
        assert str(query) == "(a) (b)"
        assert query.get_parameters() == {}

    def test_add_class_parameters(self):
        query2 = GraphQuery(clause="(b)", parameters={"c": "d"})

        query = GraphQuery(clause="(a)", parameters={"a": "b"}).add(query2)

        assert query.parameters == {"a": "b", "c": "d"}
        assert str(query) == "(a) (b)"
        assert query.get_parameters() == {"a": "b", "c": "d"}
