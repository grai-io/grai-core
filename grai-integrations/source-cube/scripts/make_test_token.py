import datetime
import os

import dotenv
import jwt

dotenv.load_dotenv()
CUBE_API_SECRET = os.environ.get("GRAI_CUBE_API_SECRET")


# Function to generate a Cube.js token without expiration
def generate_cubejs_token():
    payload = {
        "iat": datetime.datetime.now(datetime.UTC),  # Issued at time
    }

    token = jwt.encode(payload, CUBE_API_SECRET, algorithm="HS256")
    return token


def generate_user_token(user_info):
    payload = {
        "user_info": user_info,
    }

    token = jwt.encode(payload, CUBE_API_SECRET, algorithm="HS256")
    return token


# Example usage
cubejs_token = generate_cubejs_token()
print("Cube.js Token (No Expiry):", cubejs_token)

# Assuming you have a user_info object/dictionary
user_info = {"id": "user123", "role": "admin"}
user_token = generate_user_token(user_info)
print("User Token (No Expiry):", user_token)
