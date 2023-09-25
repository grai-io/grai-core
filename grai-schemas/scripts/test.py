import pydantic
from pydantic import BaseModel


class Test(pydantic.BaseModel):
    """Class definition of Test

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
