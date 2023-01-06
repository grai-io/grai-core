from connections.models import Connector, Connection, Run
from connections.tasks import run_update_server
from workspaces.models import Workspace
import pytest
from django.test import TransactionTestCase


class TestUpdateServer(TransactionTestCase):
    def test_run_update_server_postgres(self):
        workspace = Workspace.objects.create(name="W1")
        connector = Connector.objects.create(name="Postgres")
        connection = Connection.objects.create(
            name="C1",
            connector=connector,
            workspace=workspace,
            metadata={"host": "a", "port": 5432, "dbname": "grai", "user": "grai"},
            secrets={"password": "grai"},
        )
        run = Run.objects.create(connection=connection, workspace=workspace)

        with pytest.raises(Exception) as e_info:
            run_update_server(str(run.id))

        assert (
            str(e_info.value)
            == 'could not translate host name "a" to address: nodename nor servname provided, or not known\n'
            or str(e_info.value)
            == 'could not translate host name "a" to address: Temporary failure in name resolution\n'
        )

    def test_run_update_server_no_connector(self):
        workspace = Workspace.objects.create(name="W1")
        connector = Connector.objects.create(name="Connector")
        connection = Connection.objects.create(
            name="C1", connector=connector, workspace=workspace
        )
        run = Run.objects.create(connection=connection, workspace=workspace)

        with pytest.raises(Exception) as e_info:
            run_update_server(str(run.id))

        assert str(e_info.value) == "No connector found"
