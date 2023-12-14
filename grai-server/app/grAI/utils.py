from itertools import islice


def get_token_limit(model_type: str) -> int:
    OPENAI_TOKEN_LIMITS = {
        "gpt-4": 8192,
        "gpt-3.5-turbo": 4096,
        "gpt-3.5-turbo-16k": 16385,
        "gpt-4-32k": 32768,
        "gpt-4-1106-preview": 128000,
    }

    if model_type in OPENAI_TOKEN_LIMITS:
        return OPENAI_TOKEN_LIMITS[model_type]
    elif model_type.endswith("k"):
        return int(model_type.split("-")[-1]) * 1024
    elif model_type.startswith("gpt-4"):
        return 8192
    elif model_type.startswith("gpt-3.5"):
        return 4096
    else:
        return 2049


def chunker(it, size):
    iterator = iter(it)
    while chunk := list(islice(iterator, size)):
        yield chunk
