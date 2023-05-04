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
        client = dbtCloudClient(api_key=self.api_key)

        accounts = client.cloud.list_accounts()
        account = accounts["data"][0]

        manifest_obj = client.cloud.get_most_recent_run_artifact(account_id=account["id"], path="manifest.json")

        manifest = ManifestProcessor.load(manifest_obj, self.namespace)

        return manifest.adapted_nodes, manifest.adapted_edges
