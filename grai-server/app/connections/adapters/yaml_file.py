from itertools import tee
from typing import Sequence

from grai_schemas.schema import Schema
from grai_schemas.serializers import GraiYamlSerializer
from grai_schemas.v1.edge import SourcedEdgeV1
from grai_schemas.v1.node import SourcedNodeV1

from connections.models import Run, RunFile
from connections.task_helpers import update

from .base import BaseAdapter

SUPPORTED_SCHEMA_TYPES = {SourcedNodeV1, SourcedEdgeV1}
SUPPORTED_SCHEMA_TYPE_NAMES = {schema.__name__ for schema in SUPPORTED_SCHEMA_TYPES}


class YamlFileAdapter(BaseAdapter):
    @staticmethod
    def process_content(self, run_file: RunFile):
        file_content = GraiYamlSerializer.load(run_file.file)
        if isinstance(file_content, Sequence):
            for item in file_content:
                yield Schema(entity=item).entity
        else:
            yield Schema(entity=file_content).entity

    def get_nodes_and_edges(self):
        run_file = self.run.files.first()

        iter_a, iter_b = tee(self.process_content(self.run, run_file), 2)
        nodes = [obj for obj in iter_a if isinstance(obj, SourcedNodeV1)]
        edges = [obj for obj in iter_b if isinstance(obj, SourcedEdgeV1)]

        return nodes, edges

    def run_validate(self, run: Run) -> bool:
        result_types = {type(result) for result in self.process_content(run, run.files.first())}
        if not result_types.issubset(SUPPORTED_SCHEMA_TYPES):
            unsupported_types = result_types.difference(SUPPORTED_SCHEMA_TYPES)
            unsupported_typenames = [schema.__name__ for schema in unsupported_types]
            raise ValueError(
                f"The Yaml integration currently only supports uploading `{SUPPORTED_SCHEMA_TYPE_NAMES}`. "
                f"The provided file contains unsupported types: `{unsupported_typenames}`"
            )

        return True

    def run_tests(self, run: Run):
        pass

    def run_events(self, run: Run, all: bool = False):
        pass

    def run_update(self, run: Run):
        pass
