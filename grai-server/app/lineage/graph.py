from typing import List, Union


class WhereClause:
    wheres: Union[List[str], str] = []
    parameters: object = {}

    def __init__(self, wheres: Union[List[str], str] = [], parameters: object = {}):
        if isinstance(wheres, str):
            wheres = [wheres]

        self.wheres = wheres
        self.parameters = parameters

    def __str__(self) -> str:
        return "WHERE " + " AND ".join(self.wheres)


Clause = Union[WhereClause, str]


class GraphQuery:
    clauses: List[Clause] = []
    parameters: object = {}

    def __init__(self, clauses: List[Clause] = [], parameters: object = {}):
        self.clauses = clauses
        self.parameters = parameters

    def add(self, new: Union["GraphQuery", str]) -> "GraphQuery":
        if isinstance(new, str):
            self.clauses.append(new)

            return self

        self.clauses.extend(new.clauses)
        self.parameters = self.parameters | new.parameters

        return self

    def get_parameters(self):
        res = self.parameters

        for clause in self.clauses:
            if isinstance(clause, WhereClause):
                res = res | clause.parameters

        return res

    def __str__(self) -> str:
        return " ".join([str(clause) for clause in self.clauses])
