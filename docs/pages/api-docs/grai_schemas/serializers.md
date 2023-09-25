---
sidebar_label: serializers
title: grai_schemas.serializers
---

## to\_ecma262

```python
def to_ecma262(dt: datetime) -> str
```

Convert a datetime to a string in ECMA-262 format

This function aims to maintain compatibility with Django default datetime behavior which itself follows the ECMA-262 standard.

**Arguments**:

- `dt` - The datetime to convert


**Returns**:

  The datetime in ECMA-262 format

## GraiEncoder Objects

```python
class GraiEncoder(JSONEncoder)
```

The default JSON encoder for Grai.

This encoder provides default serialization for a variety of datatypes including:
* Enums
* Pydantic models
* UUIDs
* Paths
* Datetimes &amp; dates
* Sets
* etc...

Which should be reused for compatibility purposes.

## dump\_json

```python
def dump_json(v, *, default: Optional[Callable] = None) -> str
```

Dump an object to JSON following Grai&#x27;s serialization rules

This uses the GraiEncoder to serialize objects to JSON.

**Arguments**:

- `v` - The object to dump
- `default` - A default function to use for serialization if extra types are required.


**Returns**:

  The JSON string

## load\_json

```python
def load_json(v: str) -> Any
```

Returns a JSON object from a string

## GraiYamlSerializer Objects

```python
class GraiYamlSerializer()
```

A YAML serializer for Grai

The GraiYamlSerializer provides a simple interface for serializing and deserializing YAML files which complies with Grai&#x27;s serialization rules.

### load

```python
@staticmethod
def load(stream: Union[str, Path, IO]) -> Union[Dict, List[Dict]]
```

**Arguments**:

- `stream` - The stream to load from. This can be a string, a Path, or a file-like object.


**Returns**:

  Either a dictionary or a list of dictionaries depending on the input

### dump

```python
@classmethod
def dump(cls, item: Any, stream: Optional[Union[IO, str, Path]] = None) -> str
```

Dump an object to YAML following Grai&#x27;s serialization rules

**Arguments**:

- `item` - The object to dump
- `stream` - The stream to dump to. If None, the result is returned as a string.


**Returns**:

  The YAML string


### prep\_data

```python
@staticmethod
def prep_data(data: Any) -> Union[str, List[str]]
```

Ensures that the data is in a format compliant with Grai&#x27;s serialization rules.

**Arguments**:

- `data` - The data to prepare


**Returns**:

  If the data is a sequence, a list of strings is returned. Otherwise, a string is returned.
