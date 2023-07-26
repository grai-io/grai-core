import uuid

import pytest

from lineage.models import Node, Source
from lineage.signals import post_m2m_changed
from workspaces.models import Organisation, Workspace


@pytest.mark.django_db
def test_post_m2m():
    post_m2m_changed(Node, None, "post_add", False, Node, ["1"], "test")


@pytest.mark.django_db
def test_post_m2m_incorrect_model():
    workspace = Workspace.objects.create(
        name="Test Workspace",
        organisation=Organisation.objects.create(name=str(uuid.uuid4())),
    )

    source = Source(workspace=workspace, name="Test Source")

    class Source_nodes:
        pass

    post_m2m_changed(Source_nodes, source, "post_add", False, Source, ["1"], "test")
