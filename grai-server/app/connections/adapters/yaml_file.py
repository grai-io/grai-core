from connections.models import Run
from connections.task_helpers import get_node

from .base import BaseAdapter


class YamlFileAdapter(BaseAdapter):
    def run_update(self, run: Run):
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
