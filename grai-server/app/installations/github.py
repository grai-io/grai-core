import time
from datetime import datetime
from typing import Optional

import jwt
import requests
from django.conf import settings
from ghapi.all import GhApi

from installations.models import Repository

app_id = settings.GITHUB_APP_ID
pem = settings.GITHUB_PRIVATE_KEY


class Github:
    api: GhApi = None
    owner: str
    repo: str
    installation_id: int
    test_signal_text = "<!-- grai marker text for test comments-->"

    def __init__(self, owner: str = None, repo: str = None, installation_id: int = None):
        self.owner = owner
        self.repo = repo
        self.installation_id = installation_id if installation_id is not None else self.fetch_installation_id()
        self.get_api()

    def fetch_installation_id(self):
        return Repository.objects.get(type=Repository.GITHUB, owner=self.owner, repo=self.repo).installation_id

    def generate_jwt(self) -> str:
        with open(pem, "rb") as pem_file:
            signing_key = jwt.jwk_from_pem(pem_file.read())

        payload = {"iat": int(time.time()), "exp": int(time.time()) + 600, "iss": app_id}

        jwt_instance = jwt.JWT()
        encoded_jwt = jwt_instance.encode(payload, signing_key, alg="RS256")

        return encoded_jwt

    def connect(self):
        jwt = self.generate_jwt()

        res = requests.post(
            f"https://api.github.com/app/installations/{self.installation_id}/access_tokens",
            headers={
                "Authorization": f"Bearer {jwt}",
                "Accept": "application/vnd.github+json",
            },
        )

        res.raise_for_status()

        data = res.json()

        self.token = data.get("token")
        self.expires_at = data.get("expires_at")

        if self.token is None:
            raise Exception(data.get("message"))

        self.api = GhApi(owner=self.owner, repo=self.repo, token=self.token)

    def get_api(self) -> GhApi:
        if not self.api:
            self.connect()

        return self.api

    def create_check(
        self, head_sha: str, external_id: str = None, name: str = "Grai Update", details_url: str = None, output=None
    ):
        check = self.api.checks.create(
            name=name,
            head_sha=head_sha,
            external_id=external_id,
            status="queued",
            details_url=details_url,
            output=output,
        )

        return check

    def start_check(self, check_id: int):
        return self.api.checks.update(
            check_run_id=check_id, status="in_progress", started_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        )

    def complete_check(self, check_id: int, conclusion: str = "success"):
        return self.api.checks.update(
            check_run_id=check_id,
            status="completed",
            conclusion=conclusion,
            completed_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

    def get_repos(self):
        return self.api.apps.list_repos_accessible_to_installation()["repositories"]

    @staticmethod
    def add_comment_identifier(message, identifier):
        return f"{identifier}{message}"

    def get_marked_comment(self, pr_number: str, identifier: str) -> Optional[dict]:
        current_comments = self.api.issues.list_comments(pr_number)
        # user_comments = (comment for comment in current_comments if comment["user"]["id"] == self.bot_user_id)
        for comment in current_comments:
            if identifier in comment["body"]:
                return comment

        return None

    def post_comment(self, pr_number: str, message: str):
        message = self.add_comment_identifier(message, self.test_signal_text)

        marked_comment = self.get_marked_comment(pr_number, self.test_signal_text)

        if marked_comment is None:
            self.api.issues.create_comment(pr_number, body=message)
            return

        self.api.issues.update_comment(marked_comment["id"], body=message)
