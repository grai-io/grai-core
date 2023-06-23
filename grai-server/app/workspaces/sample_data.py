import uuid
from typing import List

from django.core.files import File

from connections.models import Connection, Connector, Run, RunFile
from connections.tasks import process_run, run_connection_schedule

from .models import Workspace


class SampleData:
    connections: List[Connection] = []

    def __init__(self, workspace: Workspace):
        self.workspace = workspace

    async def generate(self):
        print("generate")

        await self.add_connections()
        await self.run_connections()
        await self.add_dbt()
        await self.add_edges()

    async def add_connections(self):
        bigquery_connector = await Connector.objects.aget(slug="bigquery")

        self.connections.append(
            await Connection.objects.acreate(
                workspace=self.workspace,
                name="Google BigQuery",
                namespace="default",
                connector=bigquery_connector,
                metadata={"dataset": "grai_bigquery_demo", "project": "grai-demo"},
                secrets={
                    "credentials": '{ "type": "service_account", "project_id": "grai-demo", "private_key_id": "808cdbe329203ca6823ca4a5298a8f1c17430a5b", "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCbGvNvBJMkv7tW\\njLeT1U/Ds7/zO5rd+Q8Fm3QHjvKp5VX1HTqo4mGqUnpavSlnf9acUHRLKXIMeuzm\\nexVWpZHXkGvMf3dR632ZkiYHopPMCuid5iQvDD5jp3wFgp2sq438wXnR0t+hnOoF\\nyk4yEfCKkdbWm4wvqOpVivwjv5Up+wV9GHIYi3gIWJsm0Ftp4ImDOx/FPNGjLWs9\\nxpXWCe9YVUO4ZFl0quThDMyuUsWi9eSF7y2GeVNaJA9Lqzj+Ybvbor8qe4PKcFS3\\n+pu9CFqIcsBU9n0xOIrkvIQt06JIL7LsBH0LrBj/LJaxIaoJYhKnJOhVRVb7/WmD\\nWGYUMa1/AgMBAAECggEAAgUcVX5MQkbC9FIZ0/GLu+M75TmJ/0kOkoafQLfyXhcQ\\nAwSx7mAgYHz5ffQHtYLbMybzFMWB6Dqzmh7RPNMkLpgBZ2Tjk2wLMzRNjXznCtm7\\nhM7p+rjgmSClw1abohOL4lZMtVhXND4caB3l3c4RAWT71MiqzzYWcy2/seF9WlIW\\n4mu1ruqUJTCpXb46mlPaR1N2J89gz32R06aiuMfrR3Yt0v5Rj+vnNZA+srLTJX19\\n6J4R2UedJ7IZIL9QBbZHxumY0jgw/GbSFV40kBk+wVuJ0E1pbX8I0gLxmMR/EwFk\\n5YyReNzEsocPDalF6rcmcSvqNZ9zsiybLkpdQ9HkDQKBgQDRQOZnfJjQd3o4rXqa\\nDe4FhOD3J3QxqP/hPtMU5IOIttZQHX32koTZZyBNgMtS+heHCIGnDpm1ram8u7vw\\nXy+1OcAx9eZs5pFuM/zTD5fD68/8bZe6X1+NQ31ENXa5jkGTaXKx+MUtp5xwi4jx\\ngRTcSKDt+PEmu6fr/OJ2O9bMRQKBgQC9wVdaWxT6uBGoY4+KTZBAwMrKzZ0/SRky\\npZR13uLqMOFlh/X3bq56nVSl4yMDljsT0lFXRctjsTNwc+h0QYXc4fXT5YtHmksI\\npv90TYQg2qK2wQ9bhHldTCJsTFGPCxLlMD8AyL6PK9hCuatxmYc0LFF5OXy8Itlb\\nqbC1c4co8wKBgCflNsh+QehlDyFlOd3LUBkvR3D3zbh2HysDvlzaYJWdPmkR5mUv\\ndDK67ba5GorcccXmAkomh3nS/WylYmSm0UK9Gv6rgl4663lWYhqfe3D4MbRP9MCs\\n1FvrhSOPCe7Ax5HiZeK2qmlU7oeqotZgpOiG1F/quZeH6bEditO9/ur9AoGAOcrA\\nyAwlf5bACgEInp6w6IfPO6UT10p0GjDD3oJbqefpPfsCtrFHAqEYPs3GxDjlFUxg\\n6augHmTBveYPThkGpBdNv5ORr+UWJTR3aPyS2U69b9usybq3G+ssML+tt1swDg17\\nosmBACniW7AgvyB7RTCaP8l6a/JRMNGluB3PdHECgYEAnB7nYBirbRkpDrRWfbiV\\n6X9iV0284NaLqLIU9Y1USCGAnv38bxlz+kNtHUX2QKpnoXwbXVr/yHH9b92teCLx\\nnL30lTZPVy9dweuybgdIwGNlyq28pirNbLXYH/zRo9YMJ0KzArpgBi8U5w1mNud3\\n0MgqDH8AZvYngs7700WDW+o=\\n-----END PRIVATE KEY-----\\n", "client_email": "grai-352@grai-demo.iam.gserviceaccount.com", "client_id": "113796530500416825812", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/grai-352%40grai-demo.iam.gserviceaccount.com" }'
                },
            )
        )

        postgres_connector = await Connector.objects.aget(slug="postgres")

        self.connections.append(
            await Connection.objects.acreate(
                workspace=self.workspace,
                name="PostgreSQL",
                namespace="prod",
                connector=postgres_connector,
                metadata={
                    "dbname": "jaffle_shop",
                    "host": "sample-database.cudyk77thtpt.us-west-2.rds.amazonaws.com",
                    "port": "5432",
                    "user": "demo",
                },
                secrets={"password": "zfYD%qW2VOfUmK1Y"},
            )
        )

    async def add_dbt(self):
        await self.add_file("workspaces/sample_data/bigquery_manifest.json", "dbt")

    async def add_edges(self):
        await self.add_file("workspaces/sample_data/bigquery_edges.yml", "yaml_file")

    async def add_file(self, file_path: str, connector_slug: str):
        local_file = open(file_path)
        file = File(local_file)

        connector = await Connector.objects.aget(slug=connector_slug)
        connection = await Connection.objects.acreate(
            connector=connector,
            workspace=self.workspace,
            name=f"{connector.name} {uuid.uuid4()}",
            temp=True,
            namespace="default",
        )
        run = await Run.objects.acreate(workspace=self.workspace, connection=connection, status="queued")
        runFile = RunFile(run=run)
        runFile.file = file
        await runFile.asave()

        local_file.close()

        process_run.delay(run.id)

    async def run_connections(self):
        for connection in self.connections:
            run_connection_schedule.delay(connection.id)
