from grai_schemas.v1 import EdgeV1, NodeV1

from connections.models import Run, RunFile
from connections.task_helpers import get_node

from .base import BaseAdapter


class YamlFileAdapter(BaseAdapter):
    def validate_file(self, run: Run, runFile: RunFile):
        import yaml
        from grai_schemas.schema import Schema

        with runFile.file.open("r") as f:
            for item in yaml.safe_load_all(f):
                spec = item["spec"]

                if not spec.get("data_sources", None):
                    spec["data_source"] = run.source.name

                yield Schema(entity=item).entity

    def run_update(self, run: Run):
        from lineage.models import Edge, Node

        runFile = run.files.first()

        entities = self.validate_file(run, runFile)

        for entity in entities:
            type = entity.type
            values = entity.spec.dict(exclude_none=True)

            Model = Node if type == "Node" else Edge

            if type == "Edge":
                values["source"] = get_node(run.workspace, values["source"])
                values["destination"] = get_node(run.workspace, values["destination"])

            values.pop("data_sources")

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
                record = Model.objects.create(**values)

            relationship = run.source.nodes if type == "Node" else run.source.edges
            relationship.add(record)

    def get_nodes_and_edges(self):
        runFile = self.run.files.first()

        entities = self.validate_file(self.run, runFile)

        nodes = []
        edges = []

        for entity in entities:
            if entity.type == "Node":
                nodes.append(NodeV1.from_spec(entity.spec))
            elif entity.type == "Edge":
                edges.append(EdgeV1.from_spec(entity.spec))

        return nodes, edges

    def run_validate(self, run: Run) -> bool:
        self.run = run

        self.get_nodes_and_edges()

        return True
