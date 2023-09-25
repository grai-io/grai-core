---
sidebar_label: generics
title: grai_schemas.generics
---

## HashableBaseModel Objects

```python
class HashableBaseModel(BaseModel)
```



## GraiBaseModel Objects

```python
class GraiBaseModel(HashableBaseModel)
```



### update

```python
def update(new_values: Dict) -> BaseModel
```

**Arguments**:

  new_values (Dict):


**Returns**:



### Config Objects

```python
class Config()
```



## PlaceHolderSchema Objects

```python
class PlaceHolderSchema(GraiBaseModel)
```

Class definition of PlaceHolderSchema

**Attributes**:

- `is_active` - todo

### root\_validator\_of\_placeholder

```python
@root_validator(pre=True)
def root_validator_of_placeholder(cls, values)
```

**Arguments**:

  values:


**Returns**:



## DefaultValue Objects

```python
class DefaultValue(GraiBaseModel)
```

Class definition of DefaultValue

**Attributes**:

- `has_default_value` - todo
- `data_type` - todo
- `default_value` - todo

### validate\_default\_value\_root

```python
@root_validator()
def validate_default_value_root(cls, values)
```

**Arguments**:

  values:


**Returns**:



## PackageConfig Objects

```python
class PackageConfig(BaseModel)
```

Class definition of PackageConfig

**Attributes**:

- `integration_name` - todo
- `metadata_id` - todo

### metadata\_id\_validation

```python
@validator("metadata_id")
def metadata_id_validation(cls, value)
```

**Arguments**:

  value:


**Returns**:



### Config Objects

```python
class Config()
```



## Metadata Objects

```python
class Metadata(GraiBaseModel)
```

### Config Objects

```python
class Config()
```



## MalformedMetadata Objects

```python
class MalformedMetadata(GraiBaseModel)
```

Class definition of MalformedMetadata

**Attributes**:

- `malformed_values` - todo

### validate\_malformed

```python
@root_validator(pre=True)
def validate_malformed(cls, v)
```



### dict

```python
def dict(*args, **kwargs)
```
