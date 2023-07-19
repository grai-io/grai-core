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



## MalformedMetadata Objects

```python
class MalformedMetadata(GraiBaseModel)
```



### validate\_malformed

```python
@root_validator(pre=True)
def validate_malformed(cls, v)
```



### dict

```python
def dict(*args, **kwargs)
```
