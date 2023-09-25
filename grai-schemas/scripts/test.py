import pydantic
from pydantic import BaseModel


class Test(pydantic.BaseModel):
    """A test

    Stuff
    More Stuff

    Other stuff

    Attributes:
        a:
        b:
        e:
    """

    a: str
    b: complex
    e: str
