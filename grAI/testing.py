import os
import uuid
from functools import cached_property, partial
from typing import Optional

import dotenv
import openai
from grai_schemas.serializers import GraiYamlSerializer
from grai_schemas.v1.edge import EdgeV1
from grai_schemas.v1.node import NodeV1
from pydantic import BaseModel

base_dir = os.path.dirname(os.path.abspath(__file__))
workspace = "Internal"
graph_data_dir = os.path.join(base_dir, "workspaces", workspace)


dotenv.load_dotenv()
openai.organization = os.getenv("OPENAI_ORG_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")


class DataPrep:
    def __init__(self, workspace_directory: str):
        self.directory = workspace_directory
        self.nodes_file = os.path.join(self.directory, "raw", "nodes.yaml")
        self.edges_file = os.path.join(self.directory, "raw", "edges.yaml")

    @cached_property
    def raw_nodes(self):
        return [NodeV1(**item) for item in GraiYamlSerializer.load(self.nodes_file)]

    @cached_property
    def raw_edges(self):
        return [EdgeV1(**item) for item in GraiYamlSerializer.load(self.edges_file)]

    @cached_property
    def nodes(self):
        return {(n.spec.namespace, n.spec.name): n for n in self.raw_nodes}

    @cached_property
    def source_edges(self):
        edge_map = {}
        for edge in self.raw_edges:
            edge_map.setdefault((edge.spec.source.namespace, edge.spec.source.name), []).append(edge)

        return edge_map

    @cached_property
    def destination_edges(self):
        edge_map = {}
        for edge in self.raw_edges:
            edge_map.setdefault((edge.spec.destination.namespace, edge.spec.destination.name), []).append(edge)
        return edge_map

    def process_graph(self):
        def minimal_node(node: NodeV1):
            keys = ["name", "namespace", "id"]
            return {key: getattr(node.spec, key) for key in keys}

        def minimal_edge(edge: EdgeV1):
            result = {"source": edge.spec.source.id, "destination": edge.spec.destination.id}
            keys = ["name", "namespace", "id"]
            return result | {key: getattr(edge.spec, key) for key in keys}

        return {
            "nodes": [minimal_node(node) for node in self.raw_nodes],
            "edges": [minimal_edge(edge) for edge in self.raw_edges],
        }

    def get_graph_string(self):
        graph = self.process_graph()
        return GraiYamlSerializer.dump(graph)

    def write_graph(self):
        output_file = os.path.join(self.directory, "processed", "graph.json")
        graph = self.process_graph()
        GraiYamlSerializer.dump(graph, output_file)


class ConversationContext:
    def __init__(self, graph_context):
        self.preamble = (
            f"You are an assistant for a company trying to understand their data infrastructure. You will be provided"
            f" with a graph of the data infrastructure and asked questions about it. "
            f" The graph will come in the form of a yaml file containing nodes and edges each with a name, namespace, "
            f"and id. These objects are uniquely identified by their id and the (name, namespace) pair. \n\n"
            f"[Graph]\n"
        )
        self.graph_context = graph_context

    def context(self) -> str:
        return f"{self.preamble}{self.graph_context}"


prepper = DataPrep(graph_data_dir)


class NHopQuery:
    name: str
    namespace: str
    n: int


def one_hop_source_query(name: str, namespace: str):
    node_id = (namespace, name)
    node = prepper.nodes[node_id]
    edges = set(prepper.source_edges[node_id])
    edge_nodes = set([prepper.nodes[(edge.spec.source.namespace, edge.spec.source.name)] for edge in edges])
    return edge_nodes, edges


def n_hop_query(name: str, namespace: str, n: int = 3, final_nodes=None, final_edges=None):
    node_id = (namespace, name)

    if final_nodes is None:
        final_nodes = set([prepper.nodes[node_id]])
    if final_edges is None:
        final_edges = set()

    if n < 0:
        raise Exception("n must be greater than 0")
    elif n == 1:
        return one_hop_source_query(name, namespace)

    for edge in prepper.source_edges[node_id]:
        node, edges = n_hop_query(edge.spec.source.name, edge.spec.source.namespace, n - 1, final_nodes, final_edges)
        final_nodes.union(node)
        final_edges.union(edges)

    return final_nodes, final_edges


x = n_hop_query("public.auth_permission", "prod", 3)
breakpoint()
openai.InvalidRequestError


class Conversation:
    def __init__(self, prompt: str, model_type: str = "gpt-3.5-turbo", user: str = str(uuid.uuid4())):
        self.model_type = model_type
        self.system_context = prompt
        self.user = user

        self.messages = [
            {"role": "system", "content": self.system_context},
        ]

    @property
    def functions(self):
        return (
            [
                {
                    "name": "get_answer_for_user_query",
                    "description": "Get user answer in series of steps",
                    "parameters": StepByStepAIResponse.schema(),
                }
            ],
        )

    @property
    def model(self):
        return partial(openai.ChatCompletion.create, model=self.model_type, user=self.user, functions=self.functions)

    def request(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(model=self.model_type, messages=self.messages)

        self.messages.append({"role": "assistant", "content": response.choices[0].text})

        return response.choices[0].text


context = ConversationContext(prepper.get_graph_string())

conversation = Conversation(context.context())
breakpoint()
