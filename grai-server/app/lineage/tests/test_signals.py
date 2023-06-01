import pytest

from lineage.signals import post_m2m_changed
from lineage.models import Node, Source
from workspaces.models import Organisation, Workspace


@pytest.mark.django_db
def test_post_m2m():
    post_m2m_changed(Node, None, "post_add", False, Node, ["1"], "test")


@pytest.mark.django_db
def test_post_m2m_incorrect_model():
    workspace = Workspace.objects.create(
        name="Test Workspace",
        organisation=Organisation.objects.create(name="Test Organisation"),
    )

    source = Source(workspace=workspace, name="Test Source")

    class Source_nodes:
        pass

    with pytest.raises(Exception) as e_info:
        post_m2m_changed(Source_nodes, source, "post_add", False, Source, ["1"], "test")

    assert str(e_info.value) == "Unexpected model type"
