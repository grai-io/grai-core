def validate_no_slash(input: str, field_name: str):
    if input is not None and "/" in input:
        raise Exception(f"{field_name} contains forward slash")
