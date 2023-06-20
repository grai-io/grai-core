from typing import List, TypeVar, Union

T = TypeVar("T")


def wrap(input: Union[T, List[T]]) -> List[T]:
    if isinstance(input, list):
        return input

    return [input]


class Where:
    where: str
    parameters: object = {}

    def __init__(self, where: str, parameters: object = {}):
        self.where = where
        self.parameters = parameters

    def __str__(self) -> str:
        return self.where


class Match:
    match: str
    optional: bool = False
    wheres: List[Where] = []
    parameters: object = {}

    def __init__(
        self,
        match: str,
        optional: bool = False,
        where: Union[str, Where, List[Where]] = [],
        parameters: object = {},
    ):
        self.match = match
        self.optional = optional

        if isinstance(where, str):
            where = Where(where)

        self.wheres = wrap(where)
        self.parameters = parameters

    def where(self, where: Union[str, Where, List[Where]]) -> "Match":
        if isinstance(where, str):
            self.wheres.append(Where(where))

            return self

        self.wheres.extend(wrap(where))

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


Clause = Union[Match, str]


class GraphQuery:
    clause: List[Clause] = []
    parameters: object = {}

    def __init__(self, clause: Union[Clause, List[Clause]] = [], parameters: object = {}):
        self.clause = wrap(clause)
        self.parameters = parameters

    def match(
        self,
        match: Union[str, Match, List[Match]],
        where: Union[str, Where, List[Where]] = [],
        parameters: object = {},
    ) -> "GraphQuery":
        self.parameters = self.parameters | parameters

        if isinstance(match, Match):
            self.clause.append(match)

            return self

        if isinstance(match, List):
            self.clause.extend(match)

            return self

        self.clause.append(Match(match, where=where))

        return self

    def where(self, where: Union[str, Where, List[Where]], parameters: object = {}) -> "GraphQuery":
        if isinstance(where, str):
            where = Where(where, parameters)

        if isinstance(last := self.clause[-1], Match):
            last.where(where)
        else:
            raise Exception("Cannot add where clause to non-match clause")

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
