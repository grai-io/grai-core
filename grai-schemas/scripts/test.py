import pydantic
from pydantic import BaseModel


class Test(pydantic.BaseModel):
    """
    Class definition of Test.

    Attributes:
        a: Description of a.
        b: Description of b.
        e: Description of e.
    """

    a: str
    b: complex
    e: str


class Test2(pydantic.BaseModel):
    """
    Class definition of Test2.

    Attributes:
        apple: Description of apple.
    """

    apple: str


class Test3(BaseModel):
    """
    Class definition of Test3.

    Attributes:
        carrot:
    """

    carrot: str


class BaseModel:
    def __init__(self):
        pass


class Test4(BaseModel):
    """
    Class definition of Test4.

    Attributes:

    """

    pass
