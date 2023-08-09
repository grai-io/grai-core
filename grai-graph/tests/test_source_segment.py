from grai_schemas.v1.mock import MockV1

from grai_graph.graph import SourceSegment

mocker = MockV1()

a, b, c = [mocker.source.source_spec(name=name) for name in "abc"]
node_spec1 = mocker.node.id_node_spec(data_sources=[a, b])
node_spec2 = mocker.node.id_node_spec(data_sources=[b])
node_spec3 = mocker.node.id_node_spec(data_sources=[c])
edge_spec = mocker.edge.id_edge_spec(source=node_spec2, destination=node_spec3)


class TestSourceSegment:
    test_nodes = [mocker.node.node(spec=node) for node in [node_spec1, node_spec2, node_spec3]]
    test_edges = [mocker.edge.edge(spec=edge) for edge in [edge_spec]]
    segment = SourceSegment(nodes=test_nodes, edges=test_edges)

    def test_cover(self):
        result = ("b", "c")
        assert self.segment.covering_set == result

    def test_node_cover_map(self):
        result = {node_spec1.id: "b", node_spec2.id: "b", node_spec3.id: "c"}
        assert self.segment.node_cover_map == result

    def test_cover_edge_map(self):
        result = {"b": ["c"]}
        assert self.segment.cover_edge_map == result
