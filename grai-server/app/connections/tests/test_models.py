import datetime
import uuid

import pytest

from connections.models import Connection, Connector, Run
from workspaces.models import Workspace


@pytest.mark.django_db
def test_run_created():
    workspace = Workspace.objects.create(name="W1")
    connector = Connector.objects.create(name="C1")
    connection = Connection.objects.create(
        workspace=workspace, connector=connector, name="Connection 1"
    )

    run = Run.objects.create(
        workspace=workspace, connection=connection, status="success"
    )

    assert run.id == uuid.UUID(str(run.id))
    assert str(run) == str(run.id)
    assert run.status == "success"
    assert isinstance(run.metadata, dict) and len(run.metadata.keys()) == 0
    assert isinstance(run.created_at, datetime.datetime)
    assert isinstance(run.updated_at, datetime.datetime)
    assert run.started_at is None
    assert run.finished_at is None
