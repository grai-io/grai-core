import pydantic
from pydantic import BaseModel


class Test(pydantic.BaseModel):
    """

    Attributes:
        a:
        b:
        c:
        e:
    """

    a: str
    b: complex
    c: int
    e: str
