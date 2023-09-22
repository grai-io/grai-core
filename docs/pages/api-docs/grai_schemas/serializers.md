---
sidebar_label: serializers
title: grai_schemas.serializers
---

## GraiYamlSerializer Objects

```python
class GraiYamlSerializer()
```

### load

```python
@staticmethod
def load(stream: Union[str, Path, IO]) -> Union[Dict, List[Dict]]
```

**Arguments**:

  stream:


**Returns**:



### dump

```python
@classmethod
def dump(cls, item: Any, stream: Optional[Union[IO, str, Path]] = None) -> str
```

**Arguments**:

  item:
  stream:


**Returns**:



### prep\_data

```python
@staticmethod
def prep_data(data: Any) -> Union[str, List[str]]
```

**Arguments**:

  data (Any):


**Returns**:
