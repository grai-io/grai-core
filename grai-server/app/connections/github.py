import time
from datetime import datetime

import jwt
import requests
from ghapi.all import GhApi
from connections.models import Repository

app_id = "215508"
pem = "/Users/edwardlouth/Desktop/graibot.2023-02-07.private-key.pem"


class Github:
    api: GhApi = None
    owner: str
    repo: str
    installation_id: int

    def __init__(self, owner: str = None, repo: str = None, installation_id: int = None):
        self.owner = owner
        self.repo = repo
        self.installation_id = installation_id if installation_id is not None else self.fetch_installation_id()

    def fetch_installation_id(self):
        return Repository.objects.get(type=Repository.GITHUB, owner=self.owner, repo=self.repo).installation_id

    def generate_jwt(self) -> str:
        with open(pem, "rb") as pem_file:
            signing_key = jwt.jwk_from_pem(pem_file.read())

        payload = {"iat": int(time.time()), "exp": int(time.time()) + 600, "iss": app_id}

        jwt_instance = jwt.JWT()
        encoded_jwt = jwt_instance.encode(payload, signing_key, alg="RS256")

        print(f"JWT: ", encoded_jwt)

        return encoded_jwt

    def connect(self):
        jwt = self.generate_jwt()

        print(f"installation_id: {self.installation_id}")

        res = requests.post(
            f"https://api.github.com/app/installations/{self.installation_id}/access_tokens",
            headers={
                "Authorization": f"Bearer {jwt}",
                "Accept": "application/vnd.github+json",
            },
        )

        data = res.json()

        print(data)

        self.token = data.get("token")
        self.expires_at = data.get("expires_at")

        if self.token is None:
            raise Exception(data.get("message"))

        self.api = GhApi(owner=self.owner, repo=self.repo, token=self.token)

    def get_api(self) -> GhApi:
        if not self.api:
            self.connect()

        return self.api

    def create_check(self, head_sha: str, external_id: str = None, name: str = "Grai Update"):
        self.get_api()

        check = self.api.checks.create(name=name, head_sha=head_sha, external_id=external_id, status="queued")

        print(check)

        return check

    def start_check(self, check_id: int):
        self.get_api()

        return self.api.checks.update(
            check_run_id=check_id, status="in_progress", started_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        )

    def complete_check(self, check_id: int, conclusion: str = "success"):
        self.get_api()

        return self.api.checks.update(
            check_run_id=check_id,
            status="completed",
            conclusion=conclusion,
            completed_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

    def get_repos(self):
        self.get_api()

        return self.api.apps.list_repos_accessible_to_installation()["repositories"]
