from pydantic import BaseModel


class Test(BaseModel):
    """
    This class represents Test.

    Attributes:
        a: Description of a.
        b: Description of b.
        e: Description of e.
    """

    a: str
    b: complex
    e: str


class Test2(BaseModel):
    apple: str
