from connections.models import Run
from connections.task_helpers import update


class BaseAdapter:
    run: Run

    def get_nodes_and_edges(self):
        raise NotImplementedError(f"No get_nodes_and_edges implemented for {type(self)}")

    def run_update(self, run: Run):
        self.run = run

        nodes, edges = self.get_nodes_and_edges()

        update(self.run.workspace, nodes)
        update(self.run.workspace, edges)
