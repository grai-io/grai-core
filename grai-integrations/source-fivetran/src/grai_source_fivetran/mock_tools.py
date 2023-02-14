import importlib
from functools import wraps
from typing import Callable, TypeVar

from grai_source_fivetran.models import Column, Edge, Table

T = TypeVar("T")


has_faker = importlib.util.find_spec("faker") is not None
if has_faker:
    from faker import Faker

    fake = Faker()


def faker_dep_wrapper(fn: Callable[..., T]):
    @wraps(fn)
    def inner(*args, **kwargs) -> T:
        if not has_faker:
            raise ModuleNotFoundError("Mock testing tools require `faker`. Try running `pip install faker`")
        return fn(*args, **kwargs)

    return inner


class MockFivetranObjects:
    @staticmethod
    @faker_dep_wrapper
    def mock_column():
        return Column(
            name=fake.name(),
            namespace=fake.color_name(),
            table_name=fake.name(),
            table_schema=fake.emoji(),
            is_primary_key=fake.boolean(),
            is_foreign_key=fake.boolean(),
            fivetran_id=fake.uuid4(),
            fivetran_table_id=fake.uuid4(),
        )

    @staticmethod
    @faker_dep_wrapper
    def mock_table():
        return Table(
            name=fake.name(),
            namespace=fake.color_name(),
            schema_name=fake.emoji(),
            fivetran_id=fake.uuid4(),
        )

    @classmethod
    @faker_dep_wrapper
    def mock_edge(cls, type: str = "cc"):
        def mock_node(type: str):
            if type == "c":
                return cls.mock_column()
            elif type == "t":
                return cls.mock_table()

        source = mock_node(type[0])
        destination = mock_node(type[1])
        return Edge(source=source, destination=destination, constraint_type="c")
