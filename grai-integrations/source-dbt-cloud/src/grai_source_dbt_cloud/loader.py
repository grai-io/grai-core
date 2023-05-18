from datetime import datetime
from typing import List, Optional

from dbtc import dbtCloudClient

from grai_source_dbt.processor import ManifestProcessor


class Event:
    def __init__(self, reference: str, date: str, status: str, metadata: dict, nodes: List[str]):
        self.reference = reference
        self.date = date
        self.status = status
        self.metadata = metadata
        self.nodes = nodes


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

    def get_events(self, last_event_date) -> List[Event]:
        self.load_client()

        account = self.get_default_acount()

        runs = self.get_runs(account_id=account["id"], last_event_date=last_event_date)

        events = []

        for run in runs:
            if last_event_date and datetime.fromisoformat(run["created_at"]) < last_event_date:
                break
            
            nodes = self.get_run_nodes(account_id=account["id"], run_id=run["id"])

            status = "success" if run["status"] == 10 else "error"

            events.append(Event(reference=run["id"], date=run["created_at"], status=status, metadata=run, nodes=nodes))

        return events

    def get_run_nodes(self, account_id: str, run_id: str) -> List[str]:
        try:
          run_results = self.client.cloud.get_run_artifact(account_id=account_id, run_id=run_id, path="run_results.json")
          manifest_obj = self.client.cloud.get_run_artifact(account_id=account_id, run_id=run_id, path="manifest.json")

          unique_ids = [result["unique_id"] for result in run_results["results"] if not result["unique_id"].startswith("test.")]

          manifest = ManifestProcessor.load(manifest_obj, self.namespace)

          return [manifest.loader.node_map[unique_id].full_name for unique_id in unique_ids]
        except:
          print(f"Something has gone wrong, no run_results.json for run {run_id}")

    def load_client(self):
        self.client = dbtCloudClient(api_key=self.api_key)

    def get_default_acount(self):
        accounts = self.client.cloud.list_accounts()

        return accounts["data"][0]

    def get_runs(self, account_id: str, last_event_date):
        runs = []

        offset = 0
        limit = 100

        while True:
            result = self.client.cloud.list_runs(account_id=account_id, order_by="-created_at", limit=limit, offset=offset)

            runs.extend(result["data"])

            if result["extra"]["pagination"]["total_count"] <= len(runs):
                break

            if last_event_date and datetime.fromisoformat(result["data"][-1]["created_at"]) < last_event_date:
                break

            offset += limit

        return runs
