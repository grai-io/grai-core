import uuid
from datetime import datetime
from typing import List

from asgiref.sync import sync_to_async
from django.core.files import File

from connections.models import Connection, Connector, Run, RunFile
from connections.tasks import process_run, run_connection_schedule
from installations.models import Branch, Commit, PullRequest, Repository
from lineage.models import Source
from users.models import User

from .models import Workspace


class SampleData:
    connections: List[Connection] = []
    postgres_connection: Connection

    def __init__(self, workspace: Workspace):
        self.workspace = workspace

    def workspace_has_connections(self) -> bool:
        connections = Connection.objects.filter(workspace=self.workspace).all()
        return len(connections) > 0

    async def generate(self):
        has_connections = await sync_to_async(self.workspace_has_connections)()
        if not has_connections:
            await self.add_connections()
            await self.run_connections()
            await self.add_dbt()
            await self.add_edges()
            await self.add_reports()

    async def add_connections(self):
        bigquery_connector = await Connector.objects.aget(slug="bigquery")
        bigquery_source = await Source.objects.acreate(
            workspace=self.workspace,
            name="Google BigQuery",
        )

        self.connections.append(
            await Connection.objects.acreate(
                workspace=self.workspace,
                name="Google BigQuery",
                namespace="default",
                connector=bigquery_connector,
                source=bigquery_source,
                metadata={"dataset": "grai_bigquery_demo", "project": "grai-demo"},
                secrets={
                    "credentials": (
                        '{ "type": "service_account", "project_id": "grai-demo", "private_key_id":'
                        ' "808cdbe329203ca6823ca4a5298a8f1c17430a5b", "private_key": "-----BEGIN PRIVATE'
                        " KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCbGvNvBJMkv7tW\\njLeT1U/Ds7/zO5rd+Q8Fm3QHjvKp5VX1HTqo4mGqUnpavSlnf9acUHRLKXIMeuzm\\nexVWpZHXkGvMf3dR632ZkiYHopPMCuid5iQvDD5jp3wFgp2sq438wXnR0t+hnOoF\\nyk4yEfCKkdbWm4wvqOpVivwjv5Up+wV9GHIYi3gIWJsm0Ftp4ImDOx/FPNGjLWs9\\nxpXWCe9YVUO4ZFl0quThDMyuUsWi9eSF7y2GeVNaJA9Lqzj+Ybvbor8qe4PKcFS3\\n+pu9CFqIcsBU9n0xOIrkvIQt06JIL7LsBH0LrBj/LJaxIaoJYhKnJOhVRVb7/WmD\\nWGYUMa1/AgMBAAECggEAAgUcVX5MQkbC9FIZ0/GLu+M75TmJ/0kOkoafQLfyXhcQ\\nAwSx7mAgYHz5ffQHtYLbMybzFMWB6Dqzmh7RPNMkLpgBZ2Tjk2wLMzRNjXznCtm7\\nhM7p+rjgmSClw1abohOL4lZMtVhXND4caB3l3c4RAWT71MiqzzYWcy2/seF9WlIW\\n4mu1ruqUJTCpXb46mlPaR1N2J89gz32R06aiuMfrR3Yt0v5Rj+vnNZA+srLTJX19\\n6J4R2UedJ7IZIL9QBbZHxumY0jgw/GbSFV40kBk+wVuJ0E1pbX8I0gLxmMR/EwFk\\n5YyReNzEsocPDalF6rcmcSvqNZ9zsiybLkpdQ9HkDQKBgQDRQOZnfJjQd3o4rXqa\\nDe4FhOD3J3QxqP/hPtMU5IOIttZQHX32koTZZyBNgMtS+heHCIGnDpm1ram8u7vw\\nXy+1OcAx9eZs5pFuM/zTD5fD68/8bZe6X1+NQ31ENXa5jkGTaXKx+MUtp5xwi4jx\\ngRTcSKDt+PEmu6fr/OJ2O9bMRQKBgQC9wVdaWxT6uBGoY4+KTZBAwMrKzZ0/SRky\\npZR13uLqMOFlh/X3bq56nVSl4yMDljsT0lFXRctjsTNwc+h0QYXc4fXT5YtHmksI\\npv90TYQg2qK2wQ9bhHldTCJsTFGPCxLlMD8AyL6PK9hCuatxmYc0LFF5OXy8Itlb\\nqbC1c4co8wKBgCflNsh+QehlDyFlOd3LUBkvR3D3zbh2HysDvlzaYJWdPmkR5mUv\\ndDK67ba5GorcccXmAkomh3nS/WylYmSm0UK9Gv6rgl4663lWYhqfe3D4MbRP9MCs\\n1FvrhSOPCe7Ax5HiZeK2qmlU7oeqotZgpOiG1F/quZeH6bEditO9/ur9AoGAOcrA\\nyAwlf5bACgEInp6w6IfPO6UT10p0GjDD3oJbqefpPfsCtrFHAqEYPs3GxDjlFUxg\\n6augHmTBveYPThkGpBdNv5ORr+UWJTR3aPyS2U69b9usybq3G+ssML+tt1swDg17\\nosmBACniW7AgvyB7RTCaP8l6a/JRMNGluB3PdHECgYEAnB7nYBirbRkpDrRWfbiV\\n6X9iV0284NaLqLIU9Y1USCGAnv38bxlz+kNtHUX2QKpnoXwbXVr/yHH9b92teCLx\\nnL30lTZPVy9dweuybgdIwGNlyq28pirNbLXYH/zRo9YMJ0KzArpgBi8U5w1mNud3\\n0MgqDH8AZvYngs7700WDW+o=\\n-----END"
                        ' PRIVATE KEY-----\\n", "client_email": "grai-352@grai-demo.iam.gserviceaccount.com",'
                        ' "client_id": "113796530500416825812", "auth_uri":'
                        ' "https://accounts.google.com/o/oauth2/auth", "token_uri":'
                        ' "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url":'
                        ' "https://www.googleapis.com/oauth2/v1/certs", "client_x509_cert_url":'
                        ' "https://www.googleapis.com/robot/v1/metadata/x509/grai-352%40grai-demo.iam.gserviceaccount.com" }'
                    )
                },
                validated=True,
            )
        )

        postgres_connector = await Connector.objects.aget(slug="postgres")
        postgres_source = await Source.objects.acreate(
            workspace=self.workspace,
            name="PostgreSQL",
        )

        self.postgres_connection = await Connection.objects.acreate(
            workspace=self.workspace,
            name="PostgreSQL",
            namespace="prod",
            connector=postgres_connector,
            source=postgres_source,
            metadata={
                "dbname": "jaffle_shop",
                "host": "sample-database.cudyk77thtpt.us-west-2.rds.amazonaws.com",
                "port": "5432",
                "user": "demo",
            },
            secrets={"password": "zfYD%qW2VOfUmK1Y"},
            validated=True,
        )

        self.connections.append(self.postgres_connection)

    async def add_dbt(self):
        await self.add_file("workspaces/sample_data/bigquery_manifest.json", "dbt")

    async def add_edges(self):
        await self.add_file("workspaces/sample_data/bigquery_edges.yml", "yaml_file")

    async def add_file(self, file_path: str, connector_slug: str):
        with open(file_path, "rb") as local_file:
            file = File(local_file)

            connector = await Connector.objects.aget(slug=connector_slug)
            source = await Source.objects.acreate(
                workspace=self.workspace,
                name=connector.name,
            )
            connection = await Connection.objects.acreate(
                connector=connector,
                source=source,
                workspace=self.workspace,
                name=f"{connector.name} {uuid.uuid4()}",
                temp=True,
                namespace="default",
            )
            run = await Run.objects.acreate(
                workspace=self.workspace,
                connection=connection,
                source=source,
                status="queued",
            )
            runFile = RunFile(run=run)
            runFile.file = file
            await runFile.asave()

        await sync_to_async(process_run)(run.id)

    async def run_connections(self):
        for connection in self.connections:
            await sync_to_async(run_connection_schedule)(connection.id)

    async def get_first_user(self):
        return await User.objects.filter(memberships__workspace=self.workspace).afirst()

    async def add_report(self, metadata={}, user: User = None, commit: Commit = None):
        await Run.objects.acreate(
            workspace=self.workspace,
            connection=self.postgres_connection,
            source=self.postgres_connection.source,
            action=Run.TESTS,
            status="success",
            user=user,
            commit=commit,
            started_at=datetime.now(),
            finished_at=datetime.now(),
            metadata=metadata,
        )

    async def add_reports(self):
        user = await self.get_first_user()

        await self.add_failing_report()
        await self.add_pass_report(user=user)

    async def add_failing_report(self):
        repository = await Repository.objects.acreate(
            type=Repository.GITHUB,
            owner="grai-io",
            repo="jaffle_shop_snowflake_demo",
            workspace=self.workspace,
        )

        branch = await Branch.objects.acreate(
            workspace=self.workspace,
            repository=repository,
            reference="demo",
        )

        pull_request = await PullRequest.objects.acreate(
            workspace=self.workspace,
            repository=repository,
            branch=branch,
            reference="1",
            title="Trigger demo",
        )

        commit = await Commit.objects.acreate(
            workspace=self.workspace,
            repository=repository,
            branch=branch,
            pull_request=pull_request,
            reference="692e5840aecbd9e8a18f28c23ba94a6a61eba589",
            title="run",
        )

        # Some failures
        await self.add_report(
            commit=commit,
            metadata={
                "results": [
                    {
                        "failing_node": {
                            "id": "3b4099a4-4e31-48a3-9eb0-3fb8a59e47ea",
                            "name": "PUBLIC.raw_customers.id",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_customers.id",
                        "message": "Node `default/PUBLIC.raw_customers.id` expected not to be unique",
                        "node": {"id": "None", "name": "prod.customers.id", "namespace": "prod"},
                        "node_name": "prod/prod.customers.id",
                        "type": "Uniqueness",
                    },
                    {
                        "failing_node": {
                            "id": "2a99fe55-4e26-4f78-894e-75de5cfa8b41",
                            "name": "PUBLIC.raw_customers.first_name",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_customers.first_name",
                        "message": "Node `default/PUBLIC.raw_customers.first_name` expected not to be nullable",
                        "node": {"id": "None", "name": "prod.customers.first_name", "namespace": "prod"},
                        "node_name": "prod/prod.customers.first_name",
                        "type": "Nullable",
                    },
                    {
                        "failing_node": {
                            "id": "d30de184-0edf-4adc-9c67-a160b859e675",
                            "name": "PUBLIC.raw_customers.last_name",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_customers.last_name",
                        "message": "Node `default/PUBLIC.raw_customers.last_name` expected not to be nullable",
                        "node": {"id": "None", "name": "prod.customers.last_name", "namespace": "prod"},
                        "node_name": "prod/prod.customers.last_name",
                        "type": "Nullable",
                    },
                    {
                        "failing_node": {
                            "id": "1790e1e7-0590-4099-ae94-4e86f2eafb81",
                            "name": "PUBLIC.raw_orders.id",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_orders.id",
                        "message": "Node `default/PUBLIC.raw_orders.id` expected not to be unique",
                        "node": {"id": "None", "name": "prod.orders.id", "namespace": "prod"},
                        "node_name": "prod/prod.orders.id",
                        "type": "Uniqueness",
                    },
                    {
                        "failing_node": {
                            "id": "2bff18b4-12c3-4ffb-8661-6d496f470e05",
                            "name": "PUBLIC.raw_orders.user_id",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_orders.user_id",
                        "message": "Node `default/PUBLIC.raw_orders.user_id` expected not to be nullable",
                        "node": {"id": "None", "name": "prod.orders.user_id", "namespace": "prod"},
                        "node_name": "prod/prod.orders.user_id",
                        "type": "Nullable",
                    },
                    {
                        "failing_node": {
                            "id": "b572f36a-21dc-45cc-855f-a204f65db0f6",
                            "name": "PUBLIC.raw_orders.order_date",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_orders.order_date",
                        "message": "Node `default/PUBLIC.raw_orders.order_date` expected not to be nullable",
                        "node": {"id": "None", "name": "prod.orders.order_date", "namespace": "prod"},
                        "node_name": "prod/prod.orders.order_date",
                        "type": "Nullable",
                        "test_pass": True,
                    },
                    {
                        "failing_node": {
                            "id": "79a35cf2-7a31-460f-8497-00cbac8c8b05",
                            "name": "PUBLIC.raw_orders.status",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_orders.status",
                        "message": "Node `default/PUBLIC.raw_orders.status` expected not to be nullable",
                        "node": {"id": "None", "name": "prod.orders.status", "namespace": "prod"},
                        "node_name": "prod/prod.orders.status",
                        "type": "Nullable",
                        "test_pass": True,
                    },
                    {
                        "failing_node": {
                            "id": "d41c38c7-2cc3-411c-8a96-2b933e9f1557",
                            "name": "PUBLIC.raw_payments.id",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_payments.id",
                        "message": "Node `default/PUBLIC.raw_payments.id` expected not to be unique",
                        "node": {"id": "None", "name": "prod.payments.id", "namespace": "prod"},
                        "node_name": "prod/prod.payments.id",
                        "type": "Uniqueness",
                        "test_pass": True,
                    },
                    {
                        "failing_node": {
                            "id": "831cbbab-ce8f-44d1-a3cf-562e921888a2",
                            "name": "PUBLIC.raw_payments.order_id",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_payments.order_id",
                        "message": "Node `default/PUBLIC.raw_payments.order_id` expected not to be nullable",
                        "node": {"id": "None", "name": "prod.payments.order_id", "namespace": "prod"},
                        "node_name": "prod/prod.payments.order_id",
                        "type": "Nullable",
                        "test_pass": True,
                    },
                    {
                        "failing_node": {
                            "id": "7e5d5764-2377-4c75-968c-a46aa2fb634e",
                            "name": "PUBLIC.raw_payments.payment_method",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_payments.payment_method",
                        "message": "Node `default/PUBLIC.raw_payments.payment_method` expected not to be nullable",
                        "node": {"id": "None", "name": "prod.payments.payment_method", "namespace": "prod"},
                        "node_name": "prod/prod.payments.payment_method",
                        "type": "Nullable",
                        "test_pass": True,
                    },
                ]
            },
        )

    async def add_pass_report(self, user: User = None):
        # All passes
        await self.add_report(
            user=user,
            metadata={
                "results": [
                    {
                        "failing_node": {
                            "id": "3b4099a4-4e31-48a3-9eb0-3fb8a59e47ea",
                            "name": "PUBLIC.raw_customers.id",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_customers.id",
                        "message": "Node `default/PUBLIC.raw_customers.id` expected not to be unique",
                        "node": {"id": "None", "name": "prod.customers.id", "namespace": "prod"},
                        "node_name": "prod/prod.customers.id",
                        "type": "Uniqueness",
                        "test_pass": True,
                    },
                    {
                        "failing_node": {
                            "id": "2a99fe55-4e26-4f78-894e-75de5cfa8b41",
                            "name": "PUBLIC.raw_customers.first_name",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_customers.first_name",
                        "message": "Node `default/PUBLIC.raw_customers.first_name` expected not to be nullable",
                        "node": {"id": "None", "name": "prod.customers.first_name", "namespace": "prod"},
                        "node_name": "prod/prod.customers.first_name",
                        "type": "Nullable",
                        "test_pass": True,
                    },
                    {
                        "failing_node": {
                            "id": "d30de184-0edf-4adc-9c67-a160b859e675",
                            "name": "PUBLIC.raw_customers.last_name",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_customers.last_name",
                        "message": "Node `default/PUBLIC.raw_customers.last_name` expected not to be nullable",
                        "node": {"id": "None", "name": "prod.customers.last_name", "namespace": "prod"},
                        "node_name": "prod/prod.customers.last_name",
                        "type": "Nullable",
                        "test_pass": True,
                    },
                    {
                        "failing_node": {
                            "id": "1790e1e7-0590-4099-ae94-4e86f2eafb81",
                            "name": "PUBLIC.raw_orders.id",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_orders.id",
                        "message": "Node `default/PUBLIC.raw_orders.id` expected not to be unique",
                        "node": {"id": "None", "name": "prod.orders.id", "namespace": "prod"},
                        "node_name": "prod/prod.orders.id",
                        "type": "Uniqueness",
                        "test_pass": True,
                    },
                    {
                        "failing_node": {
                            "id": "2bff18b4-12c3-4ffb-8661-6d496f470e05",
                            "name": "PUBLIC.raw_orders.user_id",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_orders.user_id",
                        "message": "Node `default/PUBLIC.raw_orders.user_id` expected not to be nullable",
                        "node": {"id": "None", "name": "prod.orders.user_id", "namespace": "prod"},
                        "node_name": "prod/prod.orders.user_id",
                        "type": "Nullable",
                        "test_pass": True,
                    },
                    {
                        "failing_node": {
                            "id": "b572f36a-21dc-45cc-855f-a204f65db0f6",
                            "name": "PUBLIC.raw_orders.order_date",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_orders.order_date",
                        "message": "Node `default/PUBLIC.raw_orders.order_date` expected not to be nullable",
                        "node": {"id": "None", "name": "prod.orders.order_date", "namespace": "prod"},
                        "node_name": "prod/prod.orders.order_date",
                        "type": "Nullable",
                        "test_pass": True,
                    },
                    {
                        "failing_node": {
                            "id": "79a35cf2-7a31-460f-8497-00cbac8c8b05",
                            "name": "PUBLIC.raw_orders.status",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_orders.status",
                        "message": "Node `default/PUBLIC.raw_orders.status` expected not to be nullable",
                        "node": {"id": "None", "name": "prod.orders.status", "namespace": "prod"},
                        "node_name": "prod/prod.orders.status",
                        "type": "Nullable",
                        "test_pass": True,
                    },
                    {
                        "failing_node": {
                            "id": "d41c38c7-2cc3-411c-8a96-2b933e9f1557",
                            "name": "PUBLIC.raw_payments.id",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_payments.id",
                        "message": "Node `default/PUBLIC.raw_payments.id` expected not to be unique",
                        "node": {"id": "None", "name": "prod.payments.id", "namespace": "prod"},
                        "node_name": "prod/prod.payments.id",
                        "type": "Uniqueness",
                        "test_pass": True,
                    },
                    {
                        "failing_node": {
                            "id": "831cbbab-ce8f-44d1-a3cf-562e921888a2",
                            "name": "PUBLIC.raw_payments.order_id",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_payments.order_id",
                        "message": "Node `default/PUBLIC.raw_payments.order_id` expected not to be nullable",
                        "node": {"id": "None", "name": "prod.payments.order_id", "namespace": "prod"},
                        "node_name": "prod/prod.payments.order_id",
                        "type": "Nullable",
                        "test_pass": True,
                    },
                    {
                        "failing_node": {
                            "id": "7e5d5764-2377-4c75-968c-a46aa2fb634e",
                            "name": "PUBLIC.raw_payments.payment_method",
                            "namespace": "default",
                        },
                        "failing_node_name": "default/PUBLIC.raw_payments.payment_method",
                        "message": "Node `default/PUBLIC.raw_payments.payment_method` expected not to be nullable",
                        "node": {"id": "None", "name": "prod.payments.payment_method", "namespace": "prod"},
                        "node_name": "prod/prod.payments.payment_method",
                        "type": "Nullable",
                        "test_pass": True,
                    },
                ]
            },
        )
