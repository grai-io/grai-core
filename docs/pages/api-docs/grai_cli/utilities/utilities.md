---
sidebar_label: utilities
title: grai_cli.utilities.utilities
---

## default\_callback

```python
def default_callback(ctx: typer.Context)
```

**Arguments**:

  ctx (typer.Context):


**Returns**:



## load\_yaml

```python
def load_yaml(file: Union[str, TextIOBase]) -> Dict
```

**Arguments**:

  file (Union[str, TextIOBase]):


**Returns**:



## load\_all\_yaml

```python
def load_all_yaml(file: Union[str, TextIOBase]) -> Iterable[Dict]
```

**Arguments**:

  file (Union[str, TextIOBase]):


**Returns**:



## prep\_data

```python
@multimethod
def prep_data(data: Any) -> Any
```

**Arguments**:

  data (Any):


**Returns**:



## \_

```python
@prep_data.register
def _(data: Dict) -> Dict
```

**Arguments**:

  data (Dict):


**Returns**:



## \_

```python
@prep_data.register
def _(data: UUID) -> str
```

**Arguments**:

  data (UUID):


**Returns**:



## \_

```python
@prep_data.register
def _(data: BaseModel) -> Dict
```

**Arguments**:

  data (BaseModel):


**Returns**:



## \_

```python
@prep_data.register
def _(data: List) -> List[Dict]
```

**Arguments**:

  data (List):


**Returns**:



## dump\_yaml

```python
@multimethod
def dump_yaml()
```



## dump\_individual\_yaml

```python
@dump_yaml.register
def dump_individual_yaml(item: Dict, stream: TextIOBase)
```

**Arguments**:

  item (Dict):
  stream (TextIOBase):


**Returns**:



## dump\_model\_yaml

```python
@dump_yaml.register
def dump_model_yaml(item: BaseModel, stream: TextIOBase)
```

**Arguments**:

  item (BaseModel):
  stream (TextIOBase):


**Returns**:



## dump\_multiple\_yaml

```python
@dump_yaml.register
def dump_multiple_yaml(items: Sequence[Dict], stream: TextIOBase)
```

**Arguments**:

  items (Sequence[Dict]):
  stream (TextIOBase):


**Returns**:



## dump\_multiple\_yaml

```python
@dump_yaml.register
def dump_multiple_yaml(items: Sequence[BaseModel], stream: TextIOBase)
```

**Arguments**:

  items (Sequence[BaseModel]):
  stream (TextIOBase):


**Returns**:



## write\_yaml

```python
def write_yaml(data: Union[Sequence, Dict, BaseModel],
               path: Union[str, Path, TextIOBase],
               mode: str = "w")
```

**Arguments**:

  data (Union[Sequence, Dict, BaseModel]):
  path (Union[str, Path, TextIOBase]):
- `mode` _str, optional_ - (Default value = &quot;w&quot;)


**Returns**:



## get\_config\_view

```python
def get_config_view(config_field: str)
```

Assumes &lt;config_field&gt; is dot separated i.e. `auth.username`

**Arguments**:

  config_field (str):


**Returns**:



## merge\_dicts

```python
def merge_dicts(dict_a: Dict, dict_b: Dict) -> Dict
```

Recursively merge elements of dict b into dict a preferring b

**Arguments**:

  dict_a (Dict):
  dict_b (Dict):


**Returns**:
