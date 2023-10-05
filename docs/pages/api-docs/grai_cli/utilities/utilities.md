---
sidebar_label: utilities
title: grai_cli.utilities.utilities
---

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
