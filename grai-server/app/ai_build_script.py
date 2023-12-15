import os

import tiktoken

supported_models = ["gpt-4", "gpt-4-32k", "gpt-3.5-turbo", "gpt-4-1106-preview"]

cache_dir = os.environ.get("TIKTOKEN_CACHE_DIR", None)
print("CACHE DIR: ", cache_dir)
if cache_dir is None:
    raise Exception(f"Cannot complete build with no cache directory set")
elif not os.path.exists(cache_dir):
    Exception(f"Cannot create cache directory: `{cache_dir}`")

# TODO: tiktoken doesn't seem to support cacheing multiple encoders
# for model in supported_models:
#     tiktoken.encoding_for_model(model)

tiktoken.encoding_for_model(supported_models[-1])
