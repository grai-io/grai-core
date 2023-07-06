import importlib
from functools import wraps
from typing import Callable, TypeVar

from grai_source_metabase.models import Edge, Question, Table

T = TypeVar("T")

has_faker = importlib.util.find_spec("faker") is not None
if has_faker:
    from faker import Faker

    fake = Faker()


def faker_dep_wrapper(fn: Callable[..., T]):
    """

    Args:
        fn (Callable[..., T]):

    Returns:

    Raises:

    """

    @wraps(fn)
    def inner(*args, **kwargs) -> T:
        """

        Args:
            *args:
            **kwargs:

        Returns:

        Raises:

        """
        if not has_faker:
            raise ModuleNotFoundError("Mock testing tools require `faker`. Try running `pip install faker`")
        return fn(*args, **kwargs)

    return inner


class MockMetabaseObjects:
    """ """

    @staticmethod
    @faker_dep_wrapper
    def mock_question():
        """ """
        return Question(
            name=fake.name(),
            namespace=fake.color_name(),
            description=fake.sentence(),
            database_id=fake.pyint(1, 15),
            table_id=fake.pyint(1, 10000),
            public_uuid=fake.uuid4(),
            id=fake.pyint(1, 10000),
            result_metadata=[
                {
                    "display_name": "display_name",
                    "name": "display_name",
                    "base_type": "type/Text",
                    "effective_type": "type/Text",
                    "fingerprint": {"global": {"distinct-count": 1, "nil%": 0, "sample": "sample"}},
                }
            ],
            creator={
                "id": fake.pyint(1, 2000),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
            },
            collection={
                "id": fake.pyint(1, 2000),
                "name": fake.name(),
                "color": fake.color_name(),
                "slug": fake.slug(),
                "description": fake.sentence(),
            },
        )

    @staticmethod
    @faker_dep_wrapper
    def mock_table():
        """ """
        return Table(
            name=fake.name(),
            namespace=fake.color_name(),
            id=fake.pyint(1, 10000),
            db_id=fake.pyint(1, 15),
            schema_name=fake.emoji(),
            description=fake.sentence(),
            display_name=fake.name(),
            entity_type="entity/UserTable",
            db={"id": fake.pyint(1, 15), "name": fake.name(), "engine": "postgres"},
        )

    @classmethod
    @faker_dep_wrapper
    def mock_edge(cls, type: str = "tq"):
        """

        Args:
            type (str, optional):  (Default value = "tq")

        Returns:

        Raises:

        """

        def mock_node(type: str):
            """

            Args:
                type (str):

            Returns:

            Raises:

            """
            if type == "t":
                return cls.mock_table()
            elif type == "q":
                return cls.mock_question()

        source = mock_node(type[0])
        destination = mock_node(type[1])
        return Edge(source=source, destination=destination, constraint_type="bt")
