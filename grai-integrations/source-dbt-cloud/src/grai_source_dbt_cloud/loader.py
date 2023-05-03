from typing import Callable, Dict, Iterable, List, Optional

import requests
from grai_source_dbt_cloud.dbt_cloud_api.api_models import (
    AccountsMetadataResponse,
    RunsMetadataResponse,
)
from pydantic import BaseSettings, SecretStr, validator

from grai_source_dbt.processor import ManifestProcessor


class DbtCloudConfig(BaseSettings):
    endpoint: str = "https://cloud.getdbt.com/api"
    api_key: SecretStr

    @validator("endpoint")
    def validate_endpoint(cls, value):
        return value.rstrip("/")

    class Config:
        env_prefix = "grai_fivetran_"
        env_file = ".env"


class DbtCloudAPI:
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
    ):
        passthrough_kwargs = {
            "api_key": api_key,
            "endpoint": endpoint,
        }
        self.config = DbtCloudConfig(**{k: v for k, v in passthrough_kwargs.items() if v is not None})

        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        self.session.headers.update({"Authorization": f"Token {self.config.api_key.get_secret_value()}"})
        # self.session.params.update({"limit": 10000 if limit is None else limit})

    def make_request(
        self,
        request: Callable[..., requests.Response],
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs,
    ) -> Dict:
        params = self.session.params if params is None else {**self.session.params, **params}
        headers = self.session.headers if headers is None else {**self.session.headers, **headers}
        result = request(url, params=params, headers=headers, **kwargs)
        assert result.status_code == 200
        return result.json(), result

    def paginated_query(
        self,
        request: Callable[..., requests.Response],
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs,
    ) -> Iterable[Dict]:
        result, response = self.make_request(request, url, headers=headers, params=params, **kwargs)

        return result

    def get_paginated_data_items(
        self,
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> List[Dict]:
        query = self.paginated_query(self.session.get, url, params=params, headers=headers)

        return query["data"]

    def get_accounts(self) -> List[AccountsMetadataResponse]:
        url = f"{self.config.endpoint}/v2/accounts?limit=1"
        return [AccountsMetadataResponse(**item) for item in self.get_paginated_data_items(url)]

    def get_runs(self, account_id: str) -> List[RunsMetadataResponse]:
        url = f"{self.config.endpoint}/v2/accounts/{account_id}/runs?order_by=id&status=10&limit=1"
        return [RunsMetadataResponse(**item) for item in self.get_paginated_data_items(url)]

    def get_run_artifact(self, account_id: str, run_id: str, path: str = "manifest.json"):
        url = f"{self.config.endpoint}/v2/accounts/{account_id}/runs/{run_id}/artifacts/{path}"
        data, response = self.make_request(self.session.get, url, {"Accept": "text/html"})
        return data


class DbtCloudConnector(DbtCloudAPI):
    def __init__(
        self,
        namespace: Optional[str] = "default",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.namespace = namespace

    def get_nodes_and_edges(self):
        account = self.get_accounts()[0]

        run = self.get_runs(account.id)[0]

        manifest_obj = self.get_run_artifact(account.id, run.id)

        manifest = ManifestProcessor.load(manifest_obj, self.namespace)

        return manifest.adapted_nodes, manifest.adapted_edges
