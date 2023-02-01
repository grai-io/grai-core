from datetime import datetime

from celery import shared_task

from .models import Connection, Connector, Run
from .task_helpers import get_node, update


@shared_task
def run_update_server(runId):
    print(f"Task starting {runId}")
    run = Run.objects.get(pk=runId)
    execute_run(run)


@shared_task
def run_connection_schedule(connectionId):
    connection = Connection.objects.get(pk=connectionId)
    run = Run.objects.create(workspace=connection.workspace, connection=connection, status="queued")
    execute_run(run)


def execute_run(run: Run):
    # Set run status to running
    run.status = "running"
    run.started_at = datetime.now()
    run.save()

    try:
        # update_server
        connector = run.connector

        if connector.name == Connector.POSTGRESQL:
            run_postgres(run)
        elif connector.name == Connector.SNOWFLAKE:
            run_snowflake(run)
        elif connector.name == Connector.DBT:
            run_dbt(run)
        elif connector.name == Connector.YAMLFILE:
            run_yaml_file(run)
        else:
            raise NoConnectorError(f"No connector found for: {connector.name}")

        run.status = "success"
        run.finished_at = datetime.now()
        run.save()
    except Exception as e:
        run.metadata = {"error": str(e)}
        run.status = "error"
        run.finished_at = datetime.now()
        run.save()

        raise e


def run_postgres(run: Run):
    from grai_source_postgres.base import get_nodes_and_edges
    from grai_source_postgres.loader import PostgresConnector

    metadata = run.connection.metadata
    secrets = run.connection.secrets

    conn = PostgresConnector(
        host=metadata["host"],
        port=metadata["port"],
        dbname=metadata["dbname"],
        user=metadata["user"],
        password=secrets["password"],
        namespace=run.connection.namespace,
    )
    nodes, edges = get_nodes_and_edges(conn, "v1")
    update(run.workspace, nodes)
    update(run.workspace, edges)


def run_snowflake(run: Run):
    from grai_source_snowflake.base import get_nodes_and_edges
    from grai_source_snowflake.loader import SnowflakeConnector

    metadata = run.connection.metadata
    secrets = run.connection.secrets

    conn = SnowflakeConnector(
        account=metadata.get("account"),
        user=metadata.get("user"),
        password=secrets.get("password"),
        role=metadata["role"],
        warehouse=metadata.get("warehouse"),
        database=metadata.get("database"),
        schema=metadata.get("schema"),
        namespace=run.connection.namespace,
    )
    nodes, edges = get_nodes_and_edges(conn, "v1")
    update(run.workspace, nodes)
    update(run.workspace, edges)


def run_dbt(run: Run):
    import json

    from grai_source_dbt.adapters import adapt_to_client

    # from grai_source_dbt.base import get_nodes_and_edges
    from grai_source_dbt.loader import DBTGraph, Manifest

    runFile = run.files.first()

    namespace = "default"

    # nodes, edges = get_nodes_and_edges(manifest_file=runFile.file.read(), namespace=namespace, version="v1")
    with runFile.file.open("r") as f:
        data = json.load(f)

    manifest = Manifest(**data)
    dbt_graph = DBTGraph(manifest, namespace=namespace)

    nodes = adapt_to_client(dbt_graph.nodes, "v1")
    edges = adapt_to_client(dbt_graph.edges, "v1")

    update(run.workspace, nodes)
    update(run.workspace, edges)


def run_yaml_file(run: Run):
    import yaml
    from grai_schemas.schema import Schema

    from lineage.models import Edge, Node

    runFile = run.files.first()

    def validate_file():
        with runFile.file.open("r") as f:
            for item in yaml.safe_load_all(f):
                yield Schema(entity=item).entity

    # TODO: Edges don't have a human readable unique identifier
    entities = validate_file()
    for entity in entities:
        type = entity.type
        values = entity.spec.dict(exclude_none=True)

        Model = Node if type == "Node" else Edge

        if type == "Edge":
            values["source"] = get_node(run.workspace, values["source"])
            values["destination"] = get_node(run.workspace, values["destination"])

        try:
            record = Model.objects.filter(workspace=run.workspace).get(
                name=entity.spec.name, namespace=entity.spec.namespace
            )
            provided_values = {k: v for k, v in values.items() if v}

            for key, value in provided_values.items():
                setattr(record, key, value)

            record.save()
        except Model.DoesNotExist:
            values["workspace"] = run.workspace
            Model.objects.create(**values)


class NoConnectorError(Exception):
    """raise this when no connection is found"""
