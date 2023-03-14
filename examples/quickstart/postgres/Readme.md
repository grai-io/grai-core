<div align="center">
  <img src="../../docs/assets/Grai-Logo-Horizontal-2.png" width="350px"><br>
</div>

## Introduction

In this guide we will deploy a local instance of Grai and see how to use the postgres connector to visualize data lineage for the internal Grai data model.


## Getting Started

We will first need an instance of the lineage server running

```bash
git clone https://github.com/grai-io/grai-core
cd grai-core/grai-server
docker compose up
```


We actually have two containers running right now - an instance of postgres running on port `5432` and an api server running on `8000` which  you should see it available at [http://localhost:8000](http://localhost:8000).


Let's populate grai with its own data model using the grai postgres connector. First install the connector.

```bash
pip install grai-source-postgres
```

## Connecting & Syncing

The connector comes equipped with the client library already but we will need a python terminal or Jupyter Notebook to execute a few commands to establish a connection and begin querying the server. For now we will use the default user credentials though you are free to create a new user / api keys from the server admin interface at [http://localhost:8000/admin](http://localhost:8000/admin).

```python
from grai_client.endpoints.v1.client import ClientV1

client = ClientV1('localhost', '8000', insecure=True)
client.set_authentication_headers(username='null@grai.io', password='super_secret')
```


Now that we have a client connection we can populate the server with it's own lineage.

```python
from grai_source_postgres.base import update_server

update_server(client, dbname="grai", user='grai', password='grai', namespace='test')
```

Fin. Easy right?


## Using Lineage

Now that you have lineage there are a few ways to explore your data.

#### The CLI

Install the CLI and configure your default server credentials (they will be the same as we used for the Client above.


```bash
pip install grai-cli
grai config init
```

Try a few exploratory commands like getting the current nodes in your data graph

```bash
grai get nodes
```

#### Python Library

You can also run deeper explorations using the graph library.

```python
pip install grai-graph
```

Note: If you want to see the graph visualization portions of this guide you'll need to install `graphviz` using your package manage of choice (i.e. `brew install graphviz` and the `vis` extras (i.e. `pip install 'grai-graph[vis]'`).

```python
from grai_graph import graph, analysis, visualizations

nodes = client.get('nodes')
edges = client.get('edges')

G = graph.build_graph(nodes, edges, client.id)
```

##### Counterfactuals

We can now run counterfactual analysis against our data lineage. Maybe we wanted to find out all of the data which would be impacted by deleting the `id` column on the `lineage_node` table.

```python
affected_nodes = analysis.test_delete_node(namespace='default', name='public.lineage_node.id')
for node in affected_nodes:
    print(node.spec.name)

> public.lineage_edge.source_id
> public.lineage_edge.destination_id
```

What about simply changing the data type from `uuid` to `int`?

```python
nodes = analysis.test_type_change(namespace='default', name='public.lineage_node.id', new_type='int')
for node in nodes:
    print(node.spec.name)

> public.lineage_edge.source_id
> public.lineage_edge.destination_id
```

There are also convenient plotting tools for visualizing either a part or the entirety of the graph.

```python
visualizations.plot_graph(G.relabeled_graph(), dpi=5000)
```
