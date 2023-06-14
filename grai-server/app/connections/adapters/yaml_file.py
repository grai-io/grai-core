from grai_schemas.v1 import EdgeV1, NodeV1

from connections.models import Run, RunFile
from connections.task_helpers import get_node

from .base import BaseAdapter


class YamlFileAdapter(BaseAdapter):
    def validate_file(self, runFile: RunFile):
        import yaml
        from grai_schemas.schema import Schema

        with runFile.file.open("r") as f:
            for item in yaml.safe_load_all(f):
                yield Schema(entity=item).entity

    def run_update(self, run: Run):
        from lineage.models import Edge, Node

        runFile = run.files.first()

        entities = self.validate_file(runFile)

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

    def get_nodes_and_edges(self):
        runFile = self.run.files.first()

        entities = self.validate_file(runFile)

        nodes = []
        edges = []

        for entity in entities:
            if entity.type == "Node":
                nodes.append(NodeV1.from_spec(entity.spec))
            elif entity.type == "Edge":
                edges.append(EdgeV1.from_spec(entity.spec))

        return nodes, edges
