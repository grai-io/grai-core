from uuid import UUID

import yaml
from pydantic import AnyHttpUrl, SecretStr


def uuid_serializer(dumper: yaml.Dumper, data: UUID) -> yaml.nodes.Node:
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))


def secret_str_serializer(dumper: yaml.Dumper, data: SecretStr) -> yaml.nodes.Node:
    return dumper.represent_scalar("tag:yaml.org,2002:str", data.get_secret_value())


def http_url_serializer(dumper: yaml.Dumper, data: AnyHttpUrl) -> yaml.nodes.Node:
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))


yaml.add_representer(UUID, uuid_serializer)
yaml.add_representer(SecretStr, secret_str_serializer)
yaml.add_representer(AnyHttpUrl, http_url_serializer)
