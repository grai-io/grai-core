import datetime
import os

import dotenv
import jwt

dotenv.load_dotenv()
CUBE_API_SECRET = os.environ.get("GRAI_CUBE_API_SECRET", "secret")


def generate_cubejs_token():
    payload = {"iat": datetime.datetime.now(datetime.UTC)}
    token = jwt.encode(payload, CUBE_API_SECRET, algorithm="HS256")
    return token


print("Cube.js Token (No Expiry):", generate_cubejs_token())
