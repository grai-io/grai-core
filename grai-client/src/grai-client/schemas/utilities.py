from pydantic import BaseModel, root_validator



class PlaceHolderSchema(BaseModel):
    @root_validator(pre=True)
    def _(cls, values):
        message = ("Something is wrong... I can feel it 😡. You've reached a placeholder schema - "
                    "most likely the `version` of your config file doesn't exist yet.")
        raise AssertionError(message)


class BaseGraiType:
    name = None
    type = None
