from schema import Schema, And


def base_schema():
    base = {
        "version": And(str, lambda x: x == "v1"),
        "type": And(str, lambda x: x == "Node"),
    }
    return Schema(base, ignore_extra_keys=True)


