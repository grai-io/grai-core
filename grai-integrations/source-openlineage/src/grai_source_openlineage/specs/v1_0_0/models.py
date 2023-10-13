# generated by datamodel-codegen:
#   filename:  OpenLineage.json
#   timestamp: 2023-10-13T19:23:57+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import AnyUrl, BaseModel, Field


class EventType(Enum):
    START = "START"
    COMPLETE = "COMPLETE"
    ABORT = "ABORT"
    FAIL = "FAIL"
    OTHER = "OTHER"


class BaseFacet(BaseModel):
    field_producer: AnyUrl = Field(
        ...,
        alias="_producer",
        description="URI identifying the producer of this metadata. For example this could be a git url with a given tag or sha",
        example="https://github.com/OpenLineage/OpenLineage/blob/v1-0-0/client",
    )
    field_schemaURL: AnyUrl = Field(
        ...,
        alias="_schemaURL",
        description="The JSON Pointer (https://tools.ietf.org/html/rfc6901) URL to the corresponding version of the schema definition for this facet",
        example="https://openlineage.io/spec/0-0-1/OpenLineage.json#/definitions/BaseFacet",
    )


class CustomFacet(BaseFacet):
    pass


class NominalTimeRunFacet(BaseFacet):
    nominalStartTime: datetime = Field(
        ...,
        description="An [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) timestamp representing the nominal start time (included) of the run. AKA the schedule time",
        example="2020-12-17T03:00:00.000Z",
    )
    nominalEndTime: Optional[datetime] = Field(
        None,
        description="An [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) timestamp representing the nominal end time (excluded) of the run. (Should be the nominal start time of the next run)",
        example="2020-12-17T04:00:00.000Z",
    )


class Run1(BaseModel):
    runId: UUID = Field(..., description="The globally unique ID of the run associated with the job.")


class Job1(BaseModel):
    namespace: str = Field(..., description="The namespace containing that job", example="my-scheduler-namespace")
    name: str = Field(..., description="The unique name for that job within that namespace", example="myjob.mytask")


class ParentRunFacet(BaseFacet):
    run: Run1
    job: Job1


class DocumentationJobFacet(BaseFacet):
    description: str = Field(..., description="The description of the job.")


class SourceCodeLocationJobFacet(BaseFacet):
    type: str = Field(..., description="the source control system", example="git|svn")
    url: AnyUrl = Field(
        ...,
        description="the full http URL to locate the file",
        example="https://github.com/MarquezProject/marquez-airflow-quickstart/blob/693e35482bc2e526ced2b5f9f76ef83dec6ec691/dags/dummy_example.py",
    )
    repoUrl: Optional[str] = Field(
        None,
        description="the URL to the repository",
        example="git@github.com:{org}/{repo}.git or https://github.com/{org}/{repo}.git|svn://<your_ip>/<repository_name>",
    )
    path: Optional[str] = Field(
        None, description="the path in the repo containing the source files", example="path/to/my/dags"
    )
    version: Optional[str] = Field(
        None,
        description="the current version deployed (not a branch name, the actual unique version)",
        example="git: the git sha | Svn: the revision number",
    )
    tag: Optional[str] = Field(None, description="optional tag name")
    branch: Optional[str] = Field(None, description="optional branch name")


class SQLJobFacet(BaseFacet):
    query: str = Field(..., example="SELECT * FROM foo")


class OutputStatisticsOutputDatasetFacet(BaseFacet):
    rowCount: int = Field(..., description="The number of rows written to the dataset")
    size: Optional[int] = Field(None, description="The size in bytes written to the dataset")


class ColumnMetrics(BaseModel):
    nullCount: Optional[int] = Field(
        None, description="The number of null values in this column for the rows evaluated"
    )
    distinctCount: Optional[int] = Field(
        None, description="The number of distinct values in this column for the rows evaluated"
    )
    sum: Optional[float] = Field(None, description="The total sum of values in this column for the rows evaluated")
    count: Optional[float] = Field(None, description="The number of values in this column")
    min: Optional[float] = None
    max: Optional[float] = None
    quantiles: Optional[Dict[str, float]] = Field(
        None, description="The property key is the quantile. Examples: 0.1 0.25 0.5 0.75 1"
    )


class DataQualityMetricsInputDatasetFacet(BaseFacet):
    rowCount: Optional[int] = Field(None, description="The number of rows evaluated")
    bytes: Optional[int] = Field(None, description="The size in bytes")
    columnMetrics: Dict[str, ColumnMetrics] = Field(..., description="The property key is the column name")


class DocumentationDatasetFacet(BaseFacet):
    description: str = Field(
        ..., description="The description of the dataset.", example="canonical representation of entity Foo"
    )


class FieldModel(BaseModel):
    name: str = Field(..., description="The name of the field.", example="column1")
    type: Optional[str] = Field(None, description="The type of the field.", example="VARCHAR|INT|...")
    description: Optional[str] = Field(None, description="The description of the field.")


class SchemaDatasetFacet(BaseFacet):
    fields: Optional[List[FieldModel]] = Field(None, description="The fields of the table.")


class DatasourceDatasetFacet(BaseFacet):
    name: Optional[str] = None
    uri: Optional[AnyUrl] = None


class Facets(BaseModel):
    nominalTime: Optional[NominalTimeRunFacet] = None
    parent: Optional[ParentRunFacet] = None


class Run(BaseModel):
    runId: UUID = Field(..., description="The globally unique ID of the run associated with the job.")
    facets: Optional[Facets] = Field(None, description="The run facets.")


class Facets1(BaseModel):
    documentation: Optional[DocumentationJobFacet] = None
    sourceCodeLocation: Optional[SourceCodeLocationJobFacet] = None
    sql: Optional[SQLJobFacet] = None


class Job(BaseModel):
    namespace: str = Field(..., description="The namespace containing that job", example="my-scheduler-namespace")
    name: str = Field(..., description="The unique name for that job within that namespace", example="myjob.mytask")
    facets: Optional[Facets1] = Field(None, description="The job facets.")


class InputFacets(BaseModel):
    dataQualityMetrics: Optional[DataQualityMetricsInputDatasetFacet] = None


class OutputFacets(BaseModel):
    outputStatistics: Optional[OutputStatisticsOutputDatasetFacet] = None


class Facets2(BaseModel):
    documentation: Optional[DocumentationDatasetFacet] = None
    schema_: Optional[SchemaDatasetFacet] = Field(None, alias="schema")
    dataSource: Optional[DatasourceDatasetFacet] = None


class Dataset(BaseModel):
    namespace: str = Field(..., description="The namespace containing that dataset", example="my-datasource-namespace")
    name: str = Field(
        ..., description="The unique name for that dataset within that namespace", example="instance.schema.table"
    )
    facets: Optional[Facets2] = Field(None, description="The facets for this dataset")


class InputDataset(Dataset):
    inputFacets: Optional[InputFacets] = Field(None, description="The input facets for this dataset.")


class OutputDataset(Dataset):
    outputFacets: Optional[OutputFacets] = Field(None, description="The output facets for this dataset")


class RunEvent(BaseModel):
    eventType: Optional[EventType] = Field(
        None,
        description="the current transition of the run state. It is required to issue 1 START event and 1 of [ COMPLETE, ABORT, FAIL ] event per run. Additional events with OTHER eventType can be added to the same run. For example to send additional metadata after the run is complete",
        example="START|COMPLETE|ABORT|FAIL|OTHER",
    )
    eventTime: datetime = Field(..., description="the time the event occured at")
    run: Run
    job: Job
    inputs: Optional[List[InputDataset]] = Field(None, description="The set of **input** datasets.")
    outputs: Optional[List[OutputDataset]] = Field(None, description="The set of **output** datasets.")
    producer: AnyUrl = Field(
        ...,
        description="URI identifying the producer of this metadata. For example this could be a git url with a given tag or sha",
        example="https://github.com/OpenLineage/OpenLineage/blob/v1-0-0/client",
    )
    schemaURL: AnyUrl = Field(
        ...,
        description="The JSON Pointer (https://tools.ietf.org/html/rfc6901) URL to the corresponding version of the schema definition for this RunEvent",
        example="https://openlineage.io/spec/0-0-1/OpenLineage.json",
    )


class Model(BaseModel):
    __root__: RunEvent
