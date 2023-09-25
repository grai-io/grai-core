---
sidebar_label: generics
title: grai_schemas.generics
---

## HashableBaseModel Objects

```python
class HashableBaseModel(BaseModel)
```

A BaseModel that is hashable

## GraiBaseModel Objects

```python
class GraiBaseModel(HashableBaseModel)
```

The base class for all Grai models

This class provides a number of features which are useful for Grai models:
* hashable - this allows Grai models to be used as keys in dictionaries
* update - this allows Grai models to be updated with new values
* json_loads - this allows Grai models to be loaded from JSON
* json_dumps - this allows Grai models to be dumped to JSON

In addition there is are pydantic specific configuration changes which enforce consistent behavior across Grai Models:
* validate_all - this ensures that all fields are validated
* validate_assignment - this ensures that all fields are validated when assigned
* allow_population_by_field_name - this allows Grai models to be updated with new values by field name
* orm_mode - this allows Grai models to be used with ORMs

### update

```python
def update(new_values: Dict) -> BaseModel
```

Automatically update a Grai model with new values

Update uses the `merge` function to update the current model with new values.
Merge understands the nested structure of Grai models and will update nested models correctly.

**Arguments**:

  new_values (Dict):


**Returns**:

  An updated instance of the current model


### Config Objects

```python
class Config()
```



## PlaceHolderSchema Objects

```python
class PlaceHolderSchema(GraiBaseModel)
```

Class definition of PlaceHolderSchema

This is a placeholder schema which is used when a schema version is not yet available.
It should not be used for any other purpose.

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

- `has_default_value` - Identifies whether a default value is available
- `data_type` - The data type of the default value
- `default_value` - The default value

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

A base class for all metadata models

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

- `malformed_values` - A cache of values used to instantiate the class.

### validate\_malformed

```python
@root_validator(pre=True)
def validate_malformed(cls, v)
```



### dict

```python
def dict(*args, **kwargs)
```
