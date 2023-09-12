from typing import List, TypeVar, Union

T = TypeVar("T")


def wrap(input: Union[T, List[T]]) -> List[T]:
    if isinstance(input, list):
        return input

    return [input]


class Where:
    def __init__(self, where: str, parameters: object = None):
        self.where = where
        self.parameters = parameters if parameters else {}

    def __str__(self) -> str:
        return self.where


WhereType = Union[str, Where]
WhereArrayType = Union[WhereType, List[WhereType]]


def wrapWhere(input: WhereArrayType) -> List[Where]:
    if isinstance(input, list):
        return [Where(w) if isinstance(w, str) else w for w in input]

    return [input if isinstance(input, Where) else Where(input)]


class Match:
    def __init__(
        self,
        match: str,
        optional: bool = False,
        where: WhereArrayType | None = None,
        parameters: object = None,
    ):
        self.match = match
        self.optional = optional

        if isinstance(where, str):
            where = Where(where)

        self.wheres = wrapWhere(where) if where else []
        self.parameters = parameters if parameters else {}

    def where(self, where: WhereArrayType) -> "Match":
        if isinstance(where, str):
            self.wheres.append(Where(where))

            return self

        self.wheres.extend(wrapWhere(where))

        return self

    def __str__(self) -> str:
        return (
            ("OPTIONAL MATCH " if self.optional else "MATCH ")
            + self.match
            + ((" WHERE " + " AND ".join([str(w) for w in self.wheres])) if self.wheres else "")
        )

    def get_parameters(self):
        res = self.parameters

        for where in self.wheres:
            if isinstance(where, Where):
                res = res | where.parameters

        return res


MatchType = Union[Match, str]
MatchTypeArray = Union[MatchType, List[MatchType]]


def wrapMatch(input: MatchTypeArray, optional: bool = False, where: WhereArrayType | None = None) -> List[Match]:
    if isinstance(input, list):
        return [Match(w, optional=optional, where=where) if isinstance(w, str) else w for w in input]

    return [input if isinstance(input, Match) else Match(input, optional=optional, where=where)]


class GraphQuery:
    def __init__(
        self,
        clause: MatchTypeArray | None = None,
        parameters: object = None,
    ):
        self.clause = wrap(clause) if clause else []
        self.parameters = parameters if parameters else {}
        self.withWheres: str | None = None

    def match(
        self,
        match: MatchTypeArray,
        where: WhereArrayType | None = None,
        parameters: object = {},
    ) -> "GraphQuery":
        self.parameters = self.parameters | parameters

        matches = wrapMatch(match, where=where)
        self.clause.extend(matches)

        return self

    def optional_match(
        self,
        match: MatchTypeArray,
        where: WhereArrayType | None = None,
        parameters: object = {},
    ) -> "GraphQuery":
        self.parameters = self.parameters | parameters

        matches = wrapMatch(match, optional=True, where=where)
        self.clause.extend(matches)

        return self

    def where(self, where: WhereArrayType, parameters: object = {}) -> "GraphQuery":
        if isinstance(where, str):
            where = Where(where, parameters)

        if isinstance(last := self.clause[-1], Match):
            last.where(where)
        else:
            raise Exception("Cannot add where clause to non-match clause")

        return self

    def withWhere(self, where: str) -> "GraphQuery":
        self.withWheres = where

        return self

    def add(self, new: Union["GraphQuery", str]) -> "GraphQuery":
        if isinstance(new, str):
            self.clause.append(new)

            return self

        self.clause.extend(new.clause)
        self.parameters = self.parameters | new.parameters

        return self

    def get_parameters(self):
        res = self.parameters

        for clause in self.clause:
            if isinstance(clause, Match):
                res = res | clause.get_parameters()

        return res

    def __str__(self) -> str:
        return " ".join([str(clause) for clause in self.clause])
