from typing import Optional

from dbtc import dbtCloudClient

from grai_source_dbt.processor import ManifestProcessor


class DbtCloudConnector:
    def __init__(
        self,
        api_key: str,
        namespace: Optional[str] = "default",
    ):
        self.api_key = api_key
        self.namespace = namespace

    def get_nodes_and_edges(self):
        self.load_client()

        account = self.get_default_acount()

        manifest_obj = self.client.cloud.get_most_recent_run_artifact(account_id=account["id"], path="manifest.json")

        manifest = ManifestProcessor.load(manifest_obj, self.namespace)

        return manifest.adapted_nodes, manifest.adapted_edges

    def get_events(self):
        self.load_client()

        account = self.get_default_acount()

        runs = self.client.cloud.list_runs(account_id=account["id"], order_by="id", limit=100)

        return runs["data"]

    def load_client(self):
        self.client = dbtCloudClient(api_key=self.api_key)

    def get_default_acount(self):
        accounts = self.client.cloud.list_accounts()

        return accounts["data"][0]
