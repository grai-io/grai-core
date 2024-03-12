---
sidebar_label: generics
title: grai_schemas.v1.generics
---

## BaseID Objects

```python
class BaseID(GraiBaseModel)
```

Class definition of BaseID

**Attributes**:

- `id` - Optional UUID of the object
- `name` - Optional name of the object
- `namespace` - Optional namespace of the object

## NamedID Objects

```python
class NamedID(BaseID)
```

Class definition of NamedID

**Attributes**:

- `id` - Optional UUID of the object
- `name` - Name of the object
- `namespace` - Namespace of the object

## UuidID Objects

```python
class UuidID(BaseID)
```

Class definition of UuidID

**Attributes**:

- `id` - UUID of the object
- `name` - Optional name of the object
- `namespace` - Optional namespace of the object

## Python Objects

```python
class Python(ProgrammingLanguage)
```

Class representation of the Python programming language

## R Objects

```python
class R(ProgrammingLanguage)
```

Class representation of the R programming language

## SQL Objects

```python
class SQL(ProgrammingLanguage)
```

Class representation of the SQL programming language

## C Objects

```python
class C(ProgrammingLanguage)
```

Class representation of the C programming language

## CSharp Objects

```python
class CSharp(ProgrammingLanguage)
```

Class representation of the C# programming language

## CPP Objects

```python
class CPP(ProgrammingLanguage)
```

Class representation of the SQL programming language

## Java Objects

```python
class Java(ProgrammingLanguage)
```

Class representation of the Java programming language

## Scala Objects

```python
class Scala(ProgrammingLanguage)
```

Class representation of the Scala programming language

## Go Objects

```python
class Go(ProgrammingLanguage)
```

Class representation of the Go programming language

## JavaScript Objects

```python
class JavaScript(ProgrammingLanguage)
```

Class representation of the JavaScript programming language

## TypeScript Objects

```python
class TypeScript(ProgrammingLanguage)
```

Class representation of the TypeScript programming language

## Matlab Objects

```python
class Matlab(ProgrammingLanguage)
```

Class representation of the Matlab programming language

## Swift Objects

```python
class Swift(ProgrammingLanguage)
```

Class representation of the Swift programming language

## Julia Objects

```python
class Julia(ProgrammingLanguage)
```

Class representation of the Julia programming language

## SAS Objects

```python
class SAS(ProgrammingLanguage)
```

Class representation of the SAS programming language

## Rust Objects

```python
class Rust(ProgrammingLanguage)
```

Class representation of the Rust programming language

## Perl Objects

```python
class Perl(ProgrammingLanguage)
```

Class representation of the Perl programming language

## Haskell Objects

```python
class Haskell(ProgrammingLanguage)
```

Class representation of the Haskell programming language

## PHP Objects

```python
class PHP(ProgrammingLanguage)
```

Class representation of the PHP programming language

## Kotlin Objects

```python
class Kotlin(ProgrammingLanguage)
```

Class representation of the Kotlin programming language

## UnknownLanguage Objects

```python
class UnknownLanguage(ProgrammingLanguage)
```

Class representation of a catch-all programming language

## Code Objects

```python
class Code(BaseModel)
```

A generic descriptor for Code
