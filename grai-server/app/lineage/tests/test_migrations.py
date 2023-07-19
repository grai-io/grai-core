import uuid

import pytest
from django_multitenant.utils import set_current_tenant
from django_test_migrations.migrator import Migrator


class Migration0009:
    previous_state_migration = (
        "lineage",
        "0008_alter_edge_managers_alter_node_managers_and_more",
    )
    new_state_migration = ("lineage", "0009_migrate_default_lineage_types_to_generic")

    def __init__(self, migrator, old_state_spec=None, new_state_spec=None):
        self.migrator = migrator
        self.old_spec = old_state_spec if old_state_spec is not None else self.previous_state_migration
        self.new_spec = new_state_spec if new_state_spec is not None else self.new_state_migration

        self.old_state = self.migrator.apply_initial_migration(self.old_spec)
        self.new_state = None
        self.workspace = self.create_workspace()

    def reset(self):
        self.migrator.reset()

    def apply_new_state(self):
        self.new_state = self.migrator.apply_tested_migration(self.new_spec)

    def create_organisation(self, name: str = None):
        organisation = self.old_state.apps.get_model("workspaces", "Organisation")
        return organisation.objects.create(name=str(uuid.uuid4()) if name is None else name)

    def create_workspace(self, organisation=None, name: str = None):
        workspace = self.old_state.apps.get_model("workspaces", "Workspace")

        # This is a hack required by multitenant https://github.com/citusdata/django-multitenant/issues/138
        setattr(workspace, "tenant_id", "id")
        return workspace.objects.create(
            name=str(uuid.uuid4()) if name is None else name,
            organisation=organisation if organisation is not None else self.create_organisation(),
        )

    def create_node(self, node, metadata=None):
        node_data = {
            "name": str(uuid.uuid4()),
            "namespace": "test",
            "data_source": "test",
            "workspace": self.workspace,
            "metadata": {"grai": {"node_type": "Node"}} if metadata is None else metadata,
        }
        return node.objects.create(**node_data)

    def create_edge(self, node, edge, metadata=None):
        source = self.create_node(node)
        destination = self.create_node(node)
        edge_data = {
            "source": source,
            "destination": destination,
            "workspace": self.workspace,
            "metadata": {"grai": {"edge_type": "Edge"}} if metadata is None else metadata,
        }
        return edge.objects.create(**edge_data)


@pytest.mark.django_db()
def test_0009_forwards_node(migrator):
    set_current_tenant(None)

    migrator = Migration0009(migrator)

    node = migrator.old_state.apps.get_model("lineage", "Node")
    migrator.create_node(node)

    migrator.apply_new_state()
    node = migrator.new_state.apps.get_model("lineage", "Node")
    assert node.objects.filter(metadata__grai__node_type="Generic").exists()
    assert not node.objects.filter(metadata__grai__node_type="Node").exists()

    migrator.reset()


@pytest.mark.django_db()
def test_0009_forwards_edge(migrator):
    migrator = Migration0009(migrator)

    node = migrator.old_state.apps.get_model("lineage", "Node")
    edge = migrator.old_state.apps.get_model("lineage", "Edge")
    migrator.create_edge(node, edge)

    migrator.apply_new_state()
    edge = migrator.new_state.apps.get_model("lineage", "Edge")
    assert edge.objects.filter(metadata__grai__edge_type="Generic").exists()
    assert not edge.objects.filter(metadata__grai__edge_type="Edge").exists()

    migrator.reset()


@pytest.mark.django_db()
def test_0009_backwards_node(migrator):
    migrator = Migration0009(
        migrator,
        old_state_spec=("lineage", "0009_migrate_default_lineage_types_to_generic"),
        new_state_spec=(
            "lineage",
            "0008_alter_edge_managers_alter_node_managers_and_more",
        ),
    )
    node = migrator.old_state.apps.get_model("lineage", "Node")
    migrator.create_node(node, metadata={"grai": {"node_type": "Generic"}})

    migrator.apply_new_state()
    node = migrator.new_state.apps.get_model("lineage", "Node")

    assert node.objects.filter(metadata__grai__node_type="Node").exists()
    assert not node.objects.filter(metadata__grai__node_type="Generic").exists()

    migrator.reset()


@pytest.mark.django_db()
def test_0009_backwards_edge(migrator):
    migrator = Migration0009(
        migrator,
        old_state_spec=("lineage", "0009_migrate_default_lineage_types_to_generic"),
        new_state_spec=(
            "lineage",
            "0008_alter_edge_managers_alter_node_managers_and_more",
        ),
    )
    node = migrator.old_state.apps.get_model("lineage", "Node")
    edge = migrator.old_state.apps.get_model("lineage", "Edge")
    migrator.create_edge(node, edge, metadata={"grai": {"edge_type": "Generic"}})

    migrator.apply_new_state()
    edge = migrator.new_state.apps.get_model("lineage", "Edge")

    assert edge.objects.filter(metadata__grai__edge_type="Edge").exists()
    assert not edge.objects.filter(metadata__grai__edge_type="Generic").exists()

    migrator.reset()
