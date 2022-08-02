from typing import Any, Union, Literal, List, Optional
from uuid import UUID

import requests
from grai_client.endpoints.utilities import response_status_check
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.edge import EdgeLabels, EdgeV1
from grai_client.schemas.node import NodeLabels, NodeV1, NodeID
from multimethod import multimethod


@ClientV1.get_url.register
def get_node_url(client: ClientV1, obj: NodeID) -> str:
    base_url = client.node_endpoint
    return base_url


@ClientV1.get_url.register
def get_node_url(client: ClientV1, obj: NodeV1) -> str:
    return client.node_endpoint


@ClientV1.get_url.register
def get_edge_url(client: ClientV1, obj: EdgeV1) -> str:
    return client.edge_endpoint


@ClientV1.get_url.register
def get_edge_url(client: ClientV1, obj: NodeLabels) -> str:
    return client.node_endpoint


@ClientV1.get_url.register
def get_edge_url(client: ClientV1, obj: EdgeLabels) -> str:
    return client.edge_endpoint
