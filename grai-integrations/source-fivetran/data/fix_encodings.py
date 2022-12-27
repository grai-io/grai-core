import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
file = os.path.join(dir_path, "swagger.json")
output_file = os.path.join(dir_path, "processed.json")

with open(file) as f:
    obj = json.load(f)

with open(output_file, "w", encoding="UTF-8") as f:
    json.dump(obj, f)
