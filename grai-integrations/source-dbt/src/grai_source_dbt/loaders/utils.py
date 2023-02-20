from pydantic import BaseModel


def get_schema_id_from_version(label: str) -> str:
    return label.split("/")[-1].split(".")[0]


class GraiExtras(BaseModel):
    namespace: str
    full_name: str
