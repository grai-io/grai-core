import importlib
from functools import wraps
from typing import Callable, TypeVar

from grai_source_looker.models import (
    Dashboard,
    Dimension,
    Edge,
    Explore,
    Query,
    TableID,
)

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


class MockLookerObjects:
    """ """

    @staticmethod
    @faker_dep_wrapper
    def mock_query():
        """ """
        return Query(
            id=fake.random_number(),
            title=fake.name(),
            namespace=fake.color_name(),
            model=fake.name(),
            view=fake.name(),
            fields=[],
        )

    @staticmethod
    @faker_dep_wrapper
    def mock_dashboard():
        """ """
        return Dashboard(
            id=fake.random_number(),
            title=fake.name(),
            name=fake.name(),
            namespace=fake.color_name(),
            display_name=fake.name(),
        )

    @classmethod
    @faker_dep_wrapper
    def mock_edge(cls, type: str = "cc"):
        """

        Args:
            type (str, optional):  (Default value = "cc")

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
            if type == "c":
                return cls.mock_query()
            elif type == "t":
                return cls.mock_dashboard()

        source = mock_node(type[0])
        destination = mock_node(type[1])

        def toID(node):
            return TableID(
                name=node.name if hasattr(node, "name") else node.id,
                namespace=node.namespace,
                full_name=node.name if hasattr(node, "name") else node.id,
            )

        sourceID = toID(source)
        destinationID = toID(destination)

        return (
            Edge(source=sourceID, destination=destinationID, constraint_type="f"),
            source,
            destination,
        )
