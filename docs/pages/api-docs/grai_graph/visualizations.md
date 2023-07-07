---
sidebar_label: visualizations
title: grai_graph.visualizations
---

## output\_graph

```python
def output_graph(graph: nx.DiGraph,
                 file_name: Union[Path, str],
                 sort: bool = True,
                 file_format=None,
                 dpi: Optional[int] = 800) -> None
```

Output a graph to a file, either as image or as dot file.

**Arguments**:

- `graph` _nx.DiGraph_ - the DiGraph to write or plot
- `file_name` _Union[Path, str]_ - the file name to write to.
- `sort` _bool, optional_ - create a copy of the graph with sorted keys (Default value = True)
- `file_format` - graphviz output format, if None, the file_name extension is used as format
  https://graphviz.org/doc/info/output.html (Default value = None)
- `dpi` _Optional[int], optional_ - (Default value = 800)


**Returns**:



**Raises**:

  ValueError when the file_name does not end on .svg, .png or .dot

## plot\_graph

```python
def plot_graph(graph: nx.DiGraph,
               dpi: int = 800,
               figsize: Optional[Tuple[int, int]] = None)
```

**Arguments**:

- `graph` _nx.DiGraph_ - the DiGraph to write or plot
- `dpi` _int, optional_ - dpi of the matplotlib figure. (Default value = 800)
- `figsize` _Optional[Tuple[int, int]], optional_ - (Default value = None)


**Returns**:

  : Displays the image
