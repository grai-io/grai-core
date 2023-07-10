---
sidebar_label: api_models
title: grai_source_fivetran.fivetran_api.api_models
---

## TrustCertificateRequest Objects

```python
class TrustCertificateRequest(BaseModel)
```



## ConnectCardConfig Objects

```python
class ConnectCardConfig(BaseModel)
```



## NodeTypeEnum Objects

```python
class NodeTypeEnum(Enum)
```



## NodeType Objects

```python
class NodeType(BaseModel)
```



## JsonNode Objects

```python
class JsonNode(BaseModel)
```



## SyncFrequency Objects

```python
class SyncFrequency(Enum)
```



## NewConnectorRequestV1 Objects

```python
class NewConnectorRequestV1(BaseModel)
```



## CreatePbfTokenResponse Objects

```python
class CreatePbfTokenResponse(BaseModel)
```



## ConnectCardConfigRequest Objects

```python
class ConnectCardConfigRequest(BaseModel)
```



## ResyncConnectorRequest Objects

```python
class ResyncConnectorRequest(BaseModel)
```



## RunSetupTestsRequest Objects

```python
class RunSetupTestsRequest(BaseModel)
```



## SyncConnectorRequest Objects

```python
class SyncConnectorRequest(BaseModel)
```



## SyncFrequency1 Objects

```python
class SyncFrequency1(Enum)
```



## ScheduleType Objects

```python
class ScheduleType(Enum)
```



## UpdateConnectorRequest Objects

```python
class UpdateConnectorRequest(BaseModel)
```



## Alert Objects

```python
class Alert(BaseModel)
```



## ConnectCardResponse Objects

```python
class ConnectCardResponse(BaseModel)
```



## ConnectorStatusResponse Objects

```python
class ConnectorStatusResponse(BaseModel)
```



## SetupTestResultResponse Objects

```python
class SetupTestResultResponse(BaseModel)
```



## ConnectorConnectCardResponse Objects

```python
class ConnectorConnectCardResponse(BaseModel)
```



## ReloadStandardConfigRequest Objects

```python
class ReloadStandardConfigRequest(BaseModel)
```



## ColumnUpdateRequest Objects

```python
class ColumnUpdateRequest(BaseModel)
```



## SyncMode Objects

```python
class SyncMode(Enum)
```



## TableUpdateRequest Objects

```python
class TableUpdateRequest(BaseModel)
```



## SchemaChangeHandling Objects

```python
class SchemaChangeHandling(Enum)
```



## ReasonCode Objects

```python
class ReasonCode(Enum)
```



## ColumnEnabledPatchSettings Objects

```python
class ColumnEnabledPatchSettings(BaseModel)
```



## SchemaChangeHandling1 Objects

```python
class SchemaChangeHandling1(Enum)
```



## SyncMode1 Objects

```python
class SyncMode1(Enum)
```



## ReasonCode1 Objects

```python
class ReasonCode1(Enum)
```



## TableEnabledPatchSettings Objects

```python
class TableEnabledPatchSettings(BaseModel)
```



## NewDbtProjectRequest Objects

```python
class NewDbtProjectRequest(BaseModel)
```



## ScheduleType1 Objects

```python
class ScheduleType1(Enum)
```



## DaysOfWeekEnum Objects

```python
class DaysOfWeekEnum(Enum)
```



## TransformationSchedule Objects

```python
class TransformationSchedule(BaseModel)
```



## UpdateTransformationRequest Objects

```python
class UpdateTransformationRequest(BaseModel)
```



## DbtProjectDetailsResponse Objects

```python
class DbtProjectDetailsResponse(BaseModel)
```



## Status Objects

```python
class Status(Enum)
```



## TransformationDetailsResponse Objects

```python
class TransformationDetailsResponse(BaseModel)
```



## DbtProjectResponse Objects

```python
class DbtProjectResponse(BaseModel)
```



## DbtModelResponse Objects

```python
class DbtModelResponse(BaseModel)
```



## Status1 Objects

```python
class Status1(Enum)
```



## TransformationResponse Objects

```python
class TransformationResponse(BaseModel)
```



## DbtProjectTestResponse Objects

```python
class DbtProjectTestResponse(BaseModel)
```



## Region Objects

```python
class Region(Enum)
```



## NewDestinationRequest Objects

```python
class NewDestinationRequest(BaseModel)
```



## Region1 Objects

```python
class Region1(Enum)
```



## UpdateDestinationRequest Objects

```python
class UpdateDestinationRequest(BaseModel)
```



## Region2 Objects

```python
class Region2(Enum)
```



## DestinationResponse Objects

```python
class DestinationResponse(BaseModel)
```



## TrustFingerprintRequest Objects

```python
class TrustFingerprintRequest(BaseModel)
```



## AddUserToGroupRequest Objects

```python
class AddUserToGroupRequest(BaseModel)
```



## NewGroupRequest Objects

```python
class NewGroupRequest(BaseModel)
```



## UpdateGroupRequest Objects

```python
class UpdateGroupRequest(BaseModel)
```



## GroupResponse Objects

```python
class GroupResponse(BaseModel)
```



## ConnectorResponse Objects

```python
class ConnectorResponse(BaseModel)
```



## UserResponse Objects

```python
class UserResponse(BaseModel)
```



## Type Objects

```python
class Type(Enum)
```



## MetadataResponse Objects

```python
class MetadataResponse(BaseModel)
```



## RoleResponse Objects

```python
class RoleResponse(BaseModel)
```



## ColumnMetadataResponse Objects

```python
class ColumnMetadataResponse(BaseModel)
```



## SchemaMetadataResponse Objects

```python
class SchemaMetadataResponse(BaseModel)
```



## TableMetadataResponse Objects

```python
class TableMetadataResponse(BaseModel)
```



## MembershipRequest Objects

```python
class MembershipRequest(BaseModel)
```



## TeamMembershipRequest Objects

```python
class TeamMembershipRequest(BaseModel)
```



## TeamRequest Objects

```python
class TeamRequest(BaseModel)
```



## UpdateMembershipRequest Objects

```python
class UpdateMembershipRequest(BaseModel)
```



## MembershipResponse Objects

```python
class MembershipResponse(BaseModel)
```



## TeamMembershipResponse Objects

```python
class TeamMembershipResponse(BaseModel)
```



## TeamResponse Objects

```python
class TeamResponse(BaseModel)
```



## NewUserRequest Objects

```python
class NewUserRequest(BaseModel)
```



## UpdateUserRequest Objects

```python
class UpdateUserRequest(BaseModel)
```



## WebhookRequest Objects

```python
class WebhookRequest(BaseModel)
```



## WebhookTestRequest Objects

```python
class WebhookTestRequest(BaseModel)
```



## Type1 Objects

```python
class Type1(Enum)
```



## WebhookResponse Objects

```python
class WebhookResponse(BaseModel)
```



## WebhookTestResponse Objects

```python
class WebhookTestResponse(BaseModel)
```



## Config Objects

```python
class Config(BaseModel)
```



## AuroraPostgresWarehouseConfigV1 Objects

```python
class AuroraPostgresWarehouseConfigV1(BaseModel)
```



## AuroraPostgresWarehouseNewDestinationRequest Objects

```python
class AuroraPostgresWarehouseNewDestinationRequest(
        NewDestinationRequest, AuroraPostgresWarehouseConfigV1)
```



## Config1 Objects

```python
class Config1(BaseModel)
```



## AuroraWarehouseConfigV1 Objects

```python
class AuroraWarehouseConfigV1(BaseModel)
```



## AuroraWarehouseNewDestinationRequest Objects

```python
class AuroraWarehouseNewDestinationRequest(NewDestinationRequest,
                                           AuroraWarehouseConfigV1)
```



## Config2 Objects

```python
class Config2(BaseModel)
```



## AzurePostgresWarehouseConfigV1 Objects

```python
class AzurePostgresWarehouseConfigV1(BaseModel)
```



## AzurePostgresWarehouseNewDestinationRequest Objects

```python
class AzurePostgresWarehouseNewDestinationRequest(
        NewDestinationRequest, AzurePostgresWarehouseConfigV1)
```



## Config3 Objects

```python
class Config3(BaseModel)
```



## AzureSqlDataWarehouseConfigV1 Objects

```python
class AzureSqlDataWarehouseConfigV1(BaseModel)
```



## AzureSqlDataWarehouseNewDestinationRequest Objects

```python
class AzureSqlDataWarehouseNewDestinationRequest(NewDestinationRequest,
                                                 AzureSqlDataWarehouseConfigV1
                                                 )
```



## Config4 Objects

```python
class Config4(BaseModel)
```



## AzureSqlDatabaseConfigV1 Objects

```python
class AzureSqlDatabaseConfigV1(BaseModel)
```



## AzureSqlDatabaseNewDestinationRequest Objects

```python
class AzureSqlDatabaseNewDestinationRequest(NewDestinationRequest,
                                            AzureSqlDatabaseConfigV1)
```



## Config5 Objects

```python
class Config5(BaseModel)
```



## AzureSqlManagedDbWarehouseConfigV1 Objects

```python
class AzureSqlManagedDbWarehouseConfigV1(BaseModel)
```



## AzureSqlManagedDbWarehouseNewDestinationRequest Objects

```python
class AzureSqlManagedDbWarehouseNewDestinationRequest(
        NewDestinationRequest, AzureSqlManagedDbWarehouseConfigV1)
```



## Config6 Objects

```python
class Config6(BaseModel)
```



## BigQueryConfigV1 Objects

```python
class BigQueryConfigV1(BaseModel)
```



## BigQueryNewDestinationRequest Objects

```python
class BigQueryNewDestinationRequest(NewDestinationRequest, BigQueryConfigV1)
```



## Config7 Objects

```python
class Config7(BaseModel)
```



## DatabricksConfigV1 Objects

```python
class DatabricksConfigV1(BaseModel)
```



## DatabricksNewDestinationRequest Objects

```python
class DatabricksNewDestinationRequest(NewDestinationRequest,
                                      DatabricksConfigV1)
```



## Config8 Objects

```python
class Config8(BaseModel)
```



## ManagedBigQueryConfigV1 Objects

```python
class ManagedBigQueryConfigV1(BaseModel)
```



## ManagedBigQueryNewDestinationRequest Objects

```python
class ManagedBigQueryNewDestinationRequest(NewDestinationRequest,
                                           ManagedBigQueryConfigV1)
```



## Config9 Objects

```python
class Config9(BaseModel)
```



## MariaRdsWarehouseConfigV1 Objects

```python
class MariaRdsWarehouseConfigV1(BaseModel)
```



## MariaRdsWarehouseNewDestinationRequest Objects

```python
class MariaRdsWarehouseNewDestinationRequest(NewDestinationRequest,
                                             MariaRdsWarehouseConfigV1)
```



## Config10 Objects

```python
class Config10(BaseModel)
```



## MariaWarehouseConfigV1 Objects

```python
class MariaWarehouseConfigV1(BaseModel)
```



## MariaWarehouseNewDestinationRequest Objects

```python
class MariaWarehouseNewDestinationRequest(NewDestinationRequest,
                                          MariaWarehouseConfigV1)
```



## Config11 Objects

```python
class Config11(BaseModel)
```



## MysqlRdsWarehouseConfigV1 Objects

```python
class MysqlRdsWarehouseConfigV1(BaseModel)
```



## MysqlRdsWarehouseNewDestinationRequest Objects

```python
class MysqlRdsWarehouseNewDestinationRequest(NewDestinationRequest,
                                             MysqlRdsWarehouseConfigV1)
```



## Config12 Objects

```python
class Config12(BaseModel)
```



## MysqlWarehouseConfigV1 Objects

```python
class MysqlWarehouseConfigV1(BaseModel)
```



## MysqlWarehouseNewDestinationRequest Objects

```python
class MysqlWarehouseNewDestinationRequest(NewDestinationRequest,
                                          MysqlWarehouseConfigV1)
```



## Config13 Objects

```python
class Config13(BaseModel)
```



## PanoplyConfigV1 Objects

```python
class PanoplyConfigV1(BaseModel)
```



## PanoplyNewDestinationRequest Objects

```python
class PanoplyNewDestinationRequest(NewDestinationRequest, PanoplyConfigV1)
```



## Config14 Objects

```python
class Config14(BaseModel)
```



## PeriscopeWarehouseConfigV1 Objects

```python
class PeriscopeWarehouseConfigV1(BaseModel)
```



## PeriscopeWarehouseNewDestinationRequest Objects

```python
class PeriscopeWarehouseNewDestinationRequest(NewDestinationRequest,
                                              PeriscopeWarehouseConfigV1)
```



## Config15 Objects

```python
class Config15(BaseModel)
```



## PostgresGcpWarehouseConfigV1 Objects

```python
class PostgresGcpWarehouseConfigV1(BaseModel)
```



## PostgresGcpWarehouseNewDestinationRequest Objects

```python
class PostgresGcpWarehouseNewDestinationRequest(NewDestinationRequest,
                                                PostgresGcpWarehouseConfigV1)
```



## Config16 Objects

```python
class Config16(BaseModel)
```



## PostgresRdsWarehouseConfigV1 Objects

```python
class PostgresRdsWarehouseConfigV1(BaseModel)
```



## PostgresRdsWarehouseNewDestinationRequest Objects

```python
class PostgresRdsWarehouseNewDestinationRequest(NewDestinationRequest,
                                                PostgresRdsWarehouseConfigV1)
```



## Config17 Objects

```python
class Config17(BaseModel)
```



## PostgresWarehouseConfigV1 Objects

```python
class PostgresWarehouseConfigV1(BaseModel)
```



## PostgresWarehouseNewDestinationRequest Objects

```python
class PostgresWarehouseNewDestinationRequest(NewDestinationRequest,
                                             PostgresWarehouseConfigV1)
```



## Config18 Objects

```python
class Config18(BaseModel)
```



## RedshiftConfigV1 Objects

```python
class RedshiftConfigV1(BaseModel)
```



## RedshiftNewDestinationRequest Objects

```python
class RedshiftNewDestinationRequest(NewDestinationRequest, RedshiftConfigV1)
```



## Config19 Objects

```python
class Config19(BaseModel)
```



## SnowflakeConfigV1 Objects

```python
class SnowflakeConfigV1(BaseModel)
```



## SnowflakeNewDestinationRequest Objects

```python
class SnowflakeNewDestinationRequest(NewDestinationRequest, SnowflakeConfigV1)
```



## Config20 Objects

```python
class Config20(BaseModel)
```



## SqlServerRdsWarehouseConfigV1 Objects

```python
class SqlServerRdsWarehouseConfigV1(BaseModel)
```



## SqlServerRdsWarehouseNewDestinationRequest Objects

```python
class SqlServerRdsWarehouseNewDestinationRequest(NewDestinationRequest,
                                                 SqlServerRdsWarehouseConfigV1
                                                 )
```



## Config21 Objects

```python
class Config21(BaseModel)
```



## SqlServerWarehouseConfigV1 Objects

```python
class SqlServerWarehouseConfigV1(BaseModel)
```



## SqlServerWarehouseNewDestinationRequest Objects

```python
class SqlServerWarehouseNewDestinationRequest(NewDestinationRequest,
                                              SqlServerWarehouseConfigV1)
```



## AuroraPostgresWarehouseDestinationResponse Objects

```python
class AuroraPostgresWarehouseDestinationResponse(
        DestinationResponse, AuroraPostgresWarehouseConfigV1)
```



## AuroraWarehouseDestinationResponse Objects

```python
class AuroraWarehouseDestinationResponse(DestinationResponse,
                                         AuroraWarehouseConfigV1)
```



## AzurePostgresWarehouseDestinationResponse Objects

```python
class AzurePostgresWarehouseDestinationResponse(DestinationResponse,
                                                AzurePostgresWarehouseConfigV1
                                                )
```



## AzureSqlDataWarehouseDestinationResponse Objects

```python
class AzureSqlDataWarehouseDestinationResponse(DestinationResponse,
                                               AzureSqlDataWarehouseConfigV1)
```



## AzureSqlDatabaseDestinationResponse Objects

```python
class AzureSqlDatabaseDestinationResponse(DestinationResponse,
                                          AzureSqlDatabaseConfigV1)
```



## AzureSqlManagedDbWarehouseDestinationResponse Objects

```python
class AzureSqlManagedDbWarehouseDestinationResponse(
        DestinationResponse, AzureSqlManagedDbWarehouseConfigV1)
```



## BigQueryDestinationResponse Objects

```python
class BigQueryDestinationResponse(DestinationResponse, BigQueryConfigV1)
```



## DatabricksDestinationResponse Objects

```python
class DatabricksDestinationResponse(DestinationResponse, DatabricksConfigV1)
```



## ManagedBigQueryDestinationResponse Objects

```python
class ManagedBigQueryDestinationResponse(DestinationResponse,
                                         ManagedBigQueryConfigV1)
```



## MariaRdsWarehouseDestinationResponse Objects

```python
class MariaRdsWarehouseDestinationResponse(DestinationResponse,
                                           MariaRdsWarehouseConfigV1)
```



## MariaWarehouseDestinationResponse Objects

```python
class MariaWarehouseDestinationResponse(DestinationResponse,
                                        MariaWarehouseConfigV1)
```



## MysqlRdsWarehouseDestinationResponse Objects

```python
class MysqlRdsWarehouseDestinationResponse(DestinationResponse,
                                           MysqlRdsWarehouseConfigV1)
```



## MysqlWarehouseDestinationResponse Objects

```python
class MysqlWarehouseDestinationResponse(DestinationResponse,
                                        MysqlWarehouseConfigV1)
```



## PanoplyDestinationResponse Objects

```python
class PanoplyDestinationResponse(DestinationResponse, PanoplyConfigV1)
```



## PeriscopeWarehouseDestinationResponse Objects

```python
class PeriscopeWarehouseDestinationResponse(DestinationResponse,
                                            PeriscopeWarehouseConfigV1)
```



## PostgresGcpWarehouseDestinationResponse Objects

```python
class PostgresGcpWarehouseDestinationResponse(DestinationResponse,
                                              PostgresGcpWarehouseConfigV1)
```



## PostgresRdsWarehouseDestinationResponse Objects

```python
class PostgresRdsWarehouseDestinationResponse(DestinationResponse,
                                              PostgresRdsWarehouseConfigV1)
```



## PostgresWarehouseDestinationResponse Objects

```python
class PostgresWarehouseDestinationResponse(DestinationResponse,
                                           PostgresWarehouseConfigV1)
```



## RedshiftDestinationResponse Objects

```python
class RedshiftDestinationResponse(DestinationResponse, RedshiftConfigV1)
```



## SnowflakeDestinationResponse Objects

```python
class SnowflakeDestinationResponse(DestinationResponse, SnowflakeConfigV1)
```



## SqlServerRdsWarehouseDestinationResponse Objects

```python
class SqlServerRdsWarehouseDestinationResponse(DestinationResponse,
                                               SqlServerRdsWarehouseConfigV1)
```



## SqlServerWarehouseDestinationResponse Objects

```python
class SqlServerWarehouseDestinationResponse(DestinationResponse,
                                            SqlServerWarehouseConfigV1)
```



## Config22 Objects

```python
class Config22(BaseModel)
```



## ActivecampaignConfigV1 Objects

```python
class ActivecampaignConfigV1(BaseModel)
```



## ActivecampaignNewConnectorRequestV1 Objects

```python
class ActivecampaignNewConnectorRequestV1(NewConnectorRequestV1,
                                          ActivecampaignConfigV1)
```



## Config23 Objects

```python
class Config23(BaseModel)
```



## Auth Objects

```python
class Auth(BaseModel)
```



## AdjustConfigV1 Objects

```python
class AdjustConfigV1(BaseModel)
```



## AdjustNewConnectorRequestV1 Objects

```python
class AdjustNewConnectorRequestV1(NewConnectorRequestV1, AdjustConfigV1)
```



## AdobeAnalyticsConfiguration Objects

```python
class AdobeAnalyticsConfiguration(BaseModel)
```



## Config24 Objects

```python
class Config24(BaseModel)
```



## AdobeAnalyticsConfigV1 Objects

```python
class AdobeAnalyticsConfigV1(BaseModel)
```



## AdobeAnalyticsNewConnectorRequestV1 Objects

```python
class AdobeAnalyticsNewConnectorRequestV1(NewConnectorRequestV1,
                                          AdobeAnalyticsConfigV1)
```



## Config25 Objects

```python
class Config25(BaseModel)
```



## AdobeAnalyticsDataFeedConfigV1 Objects

```python
class AdobeAnalyticsDataFeedConfigV1(BaseModel)
```



## AdobeAnalyticsDataFeedNewConnectorRequestV1 Objects

```python
class AdobeAnalyticsDataFeedNewConnectorRequestV1(
        NewConnectorRequestV1, AdobeAnalyticsDataFeedConfigV1)
```



## Config26 Objects

```python
class Config26(BaseModel)
```



## AdpWorkforceNowConfigV1 Objects

```python
class AdpWorkforceNowConfigV1(BaseModel)
```



## AdpWorkforceNowNewConnectorRequestV1 Objects

```python
class AdpWorkforceNowNewConnectorRequestV1(NewConnectorRequestV1,
                                           AdpWorkforceNowConfigV1)
```



## Config27 Objects

```python
class Config27(BaseModel)
```



## ClientAccess Objects

```python
class ClientAccess(BaseModel)
```



## Auth1 Objects

```python
class Auth1(BaseModel)
```



## AdrollConfigV1 Objects

```python
class AdrollConfigV1(BaseModel)
```



## AdrollNewConnectorRequestV1 Objects

```python
class AdrollNewConnectorRequestV1(NewConnectorRequestV1, AdrollConfigV1)
```



## Config28 Objects

```python
class Config28(BaseModel)
```



## AirtableConfigV1 Objects

```python
class AirtableConfigV1(BaseModel)
```



## AirtableNewConnectorRequestV1 Objects

```python
class AirtableNewConnectorRequestV1(NewConnectorRequestV1, AirtableConfigV1)
```



## Config29 Objects

```python
class Config29(BaseModel)
```



## ClientAccess1 Objects

```python
class ClientAccess1(BaseModel)
```



## Auth2 Objects

```python
class Auth2(BaseModel)
```



## AmazonAdsConfigV1 Objects

```python
class AmazonAdsConfigV1(BaseModel)
```



## AmazonAdsNewConnectorRequestV1 Objects

```python
class AmazonAdsNewConnectorRequestV1(NewConnectorRequestV1, AmazonAdsConfigV1)
```



## ProjectCredential Objects

```python
class ProjectCredential(BaseModel)
```



## Config30 Objects

```python
class Config30(BaseModel)
```



## AmplitudeConfigV1 Objects

```python
class AmplitudeConfigV1(BaseModel)
```



## AmplitudeNewConnectorRequestV1 Objects

```python
class AmplitudeNewConnectorRequestV1(NewConnectorRequestV1, AmplitudeConfigV1)
```



## Config31 Objects

```python
class Config31(BaseModel)
```



## AnaplanConfigV1 Objects

```python
class AnaplanConfigV1(BaseModel)
```



## AnaplanNewConnectorRequestV1 Objects

```python
class AnaplanNewConnectorRequestV1(NewConnectorRequestV1, AnaplanConfigV1)
```



## Config32 Objects

```python
class Config32(BaseModel)
```



## ApacheKafkaConfigV1 Objects

```python
class ApacheKafkaConfigV1(BaseModel)
```



## ApacheKafkaNewConnectorRequestV1 Objects

```python
class ApacheKafkaNewConnectorRequestV1(NewConnectorRequestV1,
                                       ApacheKafkaConfigV1)
```



## Config33 Objects

```python
class Config33(BaseModel)
```



## Auth3 Objects

```python
class Auth3(BaseModel)
```



## AppleSearchAdsConfigV1 Objects

```python
class AppleSearchAdsConfigV1(BaseModel)
```



## AppleSearchAdsNewConnectorRequestV1 Objects

```python
class AppleSearchAdsNewConnectorRequestV1(NewConnectorRequestV1,
                                          AppleSearchAdsConfigV1)
```



## Config34 Objects

```python
class Config34(BaseModel)
```



## AppsflyerConfigV1 Objects

```python
class AppsflyerConfigV1(BaseModel)
```



## AppsflyerNewConnectorRequestV1 Objects

```python
class AppsflyerNewConnectorRequestV1(NewConnectorRequestV1, AppsflyerConfigV1)
```



## Config35 Objects

```python
class Config35(BaseModel)
```



## ClientAccess2 Objects

```python
class ClientAccess2(BaseModel)
```



## Auth4 Objects

```python
class Auth4(BaseModel)
```



## AsanaConfigV1 Objects

```python
class AsanaConfigV1(BaseModel)
```



## AsanaNewConnectorRequestV1 Objects

```python
class AsanaNewConnectorRequestV1(NewConnectorRequestV1, AsanaConfigV1)
```



## Config36 Objects

```python
class Config36(BaseModel)
```



## AuroraConfigV1 Objects

```python
class AuroraConfigV1(BaseModel)
```



## AuroraNewConnectorRequestV1 Objects

```python
class AuroraNewConnectorRequestV1(NewConnectorRequestV1, AuroraConfigV1)
```



## Config37 Objects

```python
class Config37(BaseModel)
```



## AuroraPostgresConfigV1 Objects

```python
class AuroraPostgresConfigV1(BaseModel)
```



## AuroraPostgresNewConnectorRequestV1 Objects

```python
class AuroraPostgresNewConnectorRequestV1(NewConnectorRequestV1,
                                          AuroraPostgresConfigV1)
```



## Config38 Objects

```python
class Config38(BaseModel)
```



## AwsCloudtrailConfigV1 Objects

```python
class AwsCloudtrailConfigV1(BaseModel)
```



## AwsCloudtrailNewConnectorRequestV1 Objects

```python
class AwsCloudtrailNewConnectorRequestV1(NewConnectorRequestV1,
                                         AwsCloudtrailConfigV1)
```



## Config39 Objects

```python
class Config39(BaseModel)
```



## AwsInventoryConfigV1 Objects

```python
class AwsInventoryConfigV1(BaseModel)
```



## AwsInventoryNewConnectorRequestV1 Objects

```python
class AwsInventoryNewConnectorRequestV1(NewConnectorRequestV1,
                                        AwsInventoryConfigV1)
```



## SecretsListItem Objects

```python
class SecretsListItem(BaseModel)
```



## Config40 Objects

```python
class Config40(BaseModel)
```



## AwsLambdaConfigV1 Objects

```python
class AwsLambdaConfigV1(BaseModel)
```



## AwsLambdaNewConnectorRequestV1 Objects

```python
class AwsLambdaNewConnectorRequestV1(NewConnectorRequestV1, AwsLambdaConfigV1)
```



## Config41 Objects

```python
class Config41(BaseModel)
```



## AwsMskConfigV1 Objects

```python
class AwsMskConfigV1(BaseModel)
```



## AwsMskNewConnectorRequestV1 Objects

```python
class AwsMskNewConnectorRequestV1(NewConnectorRequestV1, AwsMskConfigV1)
```



## Config42 Objects

```python
class Config42(BaseModel)
```



## AzureBlobStorageConfigV1 Objects

```python
class AzureBlobStorageConfigV1(BaseModel)
```



## AzureBlobStorageNewConnectorRequestV1 Objects

```python
class AzureBlobStorageNewConnectorRequestV1(NewConnectorRequestV1,
                                            AzureBlobStorageConfigV1)
```



## Config43 Objects

```python
class Config43(BaseModel)
```



## AzureEventHubConfigV1 Objects

```python
class AzureEventHubConfigV1(BaseModel)
```



## AzureEventHubNewConnectorRequestV1 Objects

```python
class AzureEventHubNewConnectorRequestV1(NewConnectorRequestV1,
                                         AzureEventHubConfigV1)
```



## SecretsListItem1 Objects

```python
class SecretsListItem1(BaseModel)
```



## Config44 Objects

```python
class Config44(BaseModel)
```



## AzureFunctionConfigV1 Objects

```python
class AzureFunctionConfigV1(BaseModel)
```



## AzureFunctionNewConnectorRequestV1 Objects

```python
class AzureFunctionNewConnectorRequestV1(NewConnectorRequestV1,
                                         AzureFunctionConfigV1)
```



## Config45 Objects

```python
class Config45(BaseModel)
```



## AzurePostgresConfigV1 Objects

```python
class AzurePostgresConfigV1(BaseModel)
```



## AzurePostgresNewConnectorRequestV1 Objects

```python
class AzurePostgresNewConnectorRequestV1(NewConnectorRequestV1,
                                         AzurePostgresConfigV1)
```



## Config46 Objects

```python
class Config46(BaseModel)
```



## ClientAccess3 Objects

```python
class ClientAccess3(BaseModel)
```



## Auth5 Objects

```python
class Auth5(BaseModel)
```



## AzureServiceBusConfigV1 Objects

```python
class AzureServiceBusConfigV1(BaseModel)
```



## AzureServiceBusNewConnectorRequestV1 Objects

```python
class AzureServiceBusNewConnectorRequestV1(NewConnectorRequestV1,
                                           AzureServiceBusConfigV1)
```



## Config47 Objects

```python
class Config47(BaseModel)
```



## Auth6 Objects

```python
class Auth6(BaseModel)
```



## AzureSqlDbConfigV1 Objects

```python
class AzureSqlDbConfigV1(BaseModel)
```



## AzureSqlDbNewConnectorRequestV1 Objects

```python
class AzureSqlDbNewConnectorRequestV1(NewConnectorRequestV1,
                                      AzureSqlDbConfigV1)
```



## Config48 Objects

```python
class Config48(BaseModel)
```



## Auth7 Objects

```python
class Auth7(BaseModel)
```



## AzureSqlManagedDbConfigV1 Objects

```python
class AzureSqlManagedDbConfigV1(BaseModel)
```



## AzureSqlManagedDbNewConnectorRequestV1 Objects

```python
class AzureSqlManagedDbNewConnectorRequestV1(NewConnectorRequestV1,
                                             AzureSqlManagedDbConfigV1)
```



## Config49 Objects

```python
class Config49(BaseModel)
```



## ClientAccess4 Objects

```python
class ClientAccess4(BaseModel)
```



## Auth8 Objects

```python
class Auth8(BaseModel)
```



## BingadsConfigV1 Objects

```python
class BingadsConfigV1(BaseModel)
```



## BingadsNewConnectorRequestV1 Objects

```python
class BingadsNewConnectorRequestV1(NewConnectorRequestV1, BingadsConfigV1)
```



## Config50 Objects

```python
class Config50(BaseModel)
```



## Auth9 Objects

```python
class Auth9(BaseModel)
```



## BoxConfigV1 Objects

```python
class BoxConfigV1(BaseModel)
```



## BoxNewConnectorRequestV1 Objects

```python
class BoxNewConnectorRequestV1(NewConnectorRequestV1, BoxConfigV1)
```



## Config51 Objects

```python
class Config51(BaseModel)
```



## BraintreeConfigV1 Objects

```python
class BraintreeConfigV1(BaseModel)
```



## BraintreeNewConnectorRequestV1 Objects

```python
class BraintreeNewConnectorRequestV1(NewConnectorRequestV1, BraintreeConfigV1)
```



## Config52 Objects

```python
class Config52(BaseModel)
```



## BraintreeSandboxConfigV1 Objects

```python
class BraintreeSandboxConfigV1(BaseModel)
```



## BraintreeSandboxNewConnectorRequestV1 Objects

```python
class BraintreeSandboxNewConnectorRequestV1(NewConnectorRequestV1,
                                            BraintreeSandboxConfigV1)
```



## Config53 Objects

```python
class Config53(BaseModel)
```



## BranchConfigV1 Objects

```python
class BranchConfigV1(BaseModel)
```



## BranchNewConnectorRequestV1 Objects

```python
class BranchNewConnectorRequestV1(NewConnectorRequestV1, BranchConfigV1)
```



## Config54 Objects

```python
class Config54(BaseModel)
```



## BrazeConfigV1 Objects

```python
class BrazeConfigV1(BaseModel)
```



## BrazeNewConnectorRequestV1 Objects

```python
class BrazeNewConnectorRequestV1(NewConnectorRequestV1, BrazeConfigV1)
```



## Config55 Objects

```python
class Config55(BaseModel)
```



## CloudfrontConfigV1 Objects

```python
class CloudfrontConfigV1(BaseModel)
```



## CloudfrontNewConnectorRequestV1 Objects

```python
class CloudfrontNewConnectorRequestV1(NewConnectorRequestV1,
                                      CloudfrontConfigV1)
```



## Config56 Objects

```python
class Config56(BaseModel)
```



## ConcurConfigV1 Objects

```python
class ConcurConfigV1(BaseModel)
```



## ConcurNewConnectorRequestV1 Objects

```python
class ConcurNewConnectorRequestV1(NewConnectorRequestV1, ConcurConfigV1)
```



## Config57 Objects

```python
class Config57(BaseModel)
```



## ConfluentCloudConfigV1 Objects

```python
class ConfluentCloudConfigV1(BaseModel)
```



## ConfluentCloudNewConnectorRequestV1 Objects

```python
class ConfluentCloudNewConnectorRequestV1(NewConnectorRequestV1,
                                          ConfluentCloudConfigV1)
```



## Config58 Objects

```python
class Config58(BaseModel)
```



## CoupaConfigV1 Objects

```python
class CoupaConfigV1(BaseModel)
```



## CoupaNewConnectorRequestV1 Objects

```python
class CoupaNewConnectorRequestV1(NewConnectorRequestV1, CoupaConfigV1)
```



## Config59 Objects

```python
class Config59(BaseModel)
```



## CriteoConfigV1 Objects

```python
class CriteoConfigV1(BaseModel)
```



## CriteoNewConnectorRequestV1 Objects

```python
class CriteoNewConnectorRequestV1(NewConnectorRequestV1, CriteoConfigV1)
```



## Config60 Objects

```python
class Config60(BaseModel)
```



## DelightedConfigV1 Objects

```python
class DelightedConfigV1(BaseModel)
```



## DelightedNewConnectorRequestV1 Objects

```python
class DelightedNewConnectorRequestV1(NewConnectorRequestV1, DelightedConfigV1)
```



## Config61 Objects

```python
class Config61(BaseModel)
```



## DocumentdbConfigV1 Objects

```python
class DocumentdbConfigV1(BaseModel)
```



## DocumentdbNewConnectorRequestV1 Objects

```python
class DocumentdbNewConnectorRequestV1(NewConnectorRequestV1,
                                      DocumentdbConfigV1)
```



## DimensionFilter Objects

```python
class DimensionFilter(BaseModel)
```



## Config62 Objects

```python
class Config62(BaseModel)
```



## ClientAccess5 Objects

```python
class ClientAccess5(BaseModel)
```



## Auth10 Objects

```python
class Auth10(BaseModel)
```



## DoubleClickCampaignManagerConfigV1 Objects

```python
class DoubleClickCampaignManagerConfigV1(BaseModel)
```



## DoubleClickCampaignManagerNewConnectorRequestV1 Objects

```python
class DoubleClickCampaignManagerNewConnectorRequestV1(
        NewConnectorRequestV1, DoubleClickCampaignManagerConfigV1)
```



## Config63 Objects

```python
class Config63(BaseModel)
```



## ClientAccess6 Objects

```python
class ClientAccess6(BaseModel)
```



## Auth11 Objects

```python
class Auth11(BaseModel)
```



## DoubleClickPublishersConfigV1 Objects

```python
class DoubleClickPublishersConfigV1(BaseModel)
```



## DoubleClickPublishersNewConnectorRequestV1 Objects

```python
class DoubleClickPublishersNewConnectorRequestV1(NewConnectorRequestV1,
                                                 DoubleClickPublishersConfigV1
                                                 )
```



## Auth12 Objects

```python
class Auth12(BaseModel)
```



## DriftConfigV1 Objects

```python
class DriftConfigV1(BaseModel)
```



## DriftNewConnectorRequestV1 Objects

```python
class DriftNewConnectorRequestV1(NewConnectorRequestV1, DriftConfigV1)
```



## Config64 Objects

```python
class Config64(BaseModel)
```



## ClientAccess7 Objects

```python
class ClientAccess7(BaseModel)
```



## Auth13 Objects

```python
class Auth13(BaseModel)
```



## DropboxConfigV1 Objects

```python
class DropboxConfigV1(BaseModel)
```



## DropboxNewConnectorRequestV1 Objects

```python
class DropboxNewConnectorRequestV1(NewConnectorRequestV1, DropboxConfigV1)
```



## Config65 Objects

```python
class Config65(BaseModel)
```



## ClientAccess8 Objects

```python
class ClientAccess8(BaseModel)
```



## Auth14 Objects

```python
class Auth14(BaseModel)
```



## Dynamics365ConfigV1 Objects

```python
class Dynamics365ConfigV1(BaseModel)
```



## Dynamics365NewConnectorRequestV1 Objects

```python
class Dynamics365NewConnectorRequestV1(NewConnectorRequestV1,
                                       Dynamics365ConfigV1)
```



## Config66 Objects

```python
class Config66(BaseModel)
```



## Auth15 Objects

```python
class Auth15(BaseModel)
```



## Dynamics365FoConfigV1 Objects

```python
class Dynamics365FoConfigV1(BaseModel)
```



## Dynamics365FoNewConnectorRequestV1 Objects

```python
class Dynamics365FoNewConnectorRequestV1(NewConnectorRequestV1,
                                         Dynamics365FoConfigV1)
```



## Config67 Objects

```python
class Config67(BaseModel)
```



## DynamodbConfigV1 Objects

```python
class DynamodbConfigV1(BaseModel)
```



## DynamodbNewConnectorRequestV1 Objects

```python
class DynamodbNewConnectorRequestV1(NewConnectorRequestV1, DynamodbConfigV1)
```



## Config68 Objects

```python
class Config68(BaseModel)
```



## Auth16 Objects

```python
class Auth16(BaseModel)
```



## EloquaConfigV1 Objects

```python
class EloquaConfigV1(BaseModel)
```



## EloquaNewConnectorRequestV1 Objects

```python
class EloquaNewConnectorRequestV1(NewConnectorRequestV1, EloquaConfigV1)
```



## Config69 Objects

```python
class Config69(BaseModel)
```



## EmailConfigV1 Objects

```python
class EmailConfigV1(BaseModel)
```



## EmailNewConnectorRequestV1 Objects

```python
class EmailNewConnectorRequestV1(NewConnectorRequestV1, EmailConfigV1)
```



## Config70 Objects

```python
class Config70(BaseModel)
```



## FacebookConfigV1 Objects

```python
class FacebookConfigV1(BaseModel)
```



## FacebookNewConnectorRequestV1 Objects

```python
class FacebookNewConnectorRequestV1(NewConnectorRequestV1, FacebookConfigV1)
```



## Config71 Objects

```python
class Config71(BaseModel)
```



## FacebookAdAccountConfigV1 Objects

```python
class FacebookAdAccountConfigV1(BaseModel)
```



## FacebookAdAccountNewConnectorRequestV1 Objects

```python
class FacebookAdAccountNewConnectorRequestV1(NewConnectorRequestV1,
                                             FacebookAdAccountConfigV1)
```



## CustomTable Objects

```python
class CustomTable(BaseModel)
```



## Config72 Objects

```python
class Config72(BaseModel)
```



## ClientAccess9 Objects

```python
class ClientAccess9(BaseModel)
```



## Auth17 Objects

```python
class Auth17(BaseModel)
```



## FacebookAdsConfigV1 Objects

```python
class FacebookAdsConfigV1(BaseModel)
```



## FacebookAdsNewConnectorRequestV1 Objects

```python
class FacebookAdsNewConnectorRequestV1(NewConnectorRequestV1,
                                       FacebookAdsConfigV1)
```



## Config73 Objects

```python
class Config73(BaseModel)
```



## ClientAccess10 Objects

```python
class ClientAccess10(BaseModel)
```



## Auth18 Objects

```python
class Auth18(BaseModel)
```



## FacebookPagesConfigV1 Objects

```python
class FacebookPagesConfigV1(BaseModel)
```



## FacebookPagesNewConnectorRequestV1 Objects

```python
class FacebookPagesNewConnectorRequestV1(NewConnectorRequestV1,
                                         FacebookPagesConfigV1)
```



## Config74 Objects

```python
class Config74(BaseModel)
```



## ClientAccess11 Objects

```python
class ClientAccess11(BaseModel)
```



## Auth19 Objects

```python
class Auth19(BaseModel)
```



## FinancialForceConfigV1 Objects

```python
class FinancialForceConfigV1(BaseModel)
```



## FinancialForceNewConnectorRequestV1 Objects

```python
class FinancialForceNewConnectorRequestV1(NewConnectorRequestV1,
                                          FinancialForceConfigV1)
```



## Config75 Objects

```python
class Config75(BaseModel)
```



## FivetranLogConfigV1 Objects

```python
class FivetranLogConfigV1(BaseModel)
```



## FivetranLogNewConnectorRequestV1 Objects

```python
class FivetranLogNewConnectorRequestV1(NewConnectorRequestV1,
                                       FivetranLogConfigV1)
```



## Config76 Objects

```python
class Config76(BaseModel)
```



## FreshdeskConfigV1 Objects

```python
class FreshdeskConfigV1(BaseModel)
```



## FreshdeskNewConnectorRequestV1 Objects

```python
class FreshdeskNewConnectorRequestV1(NewConnectorRequestV1, FreshdeskConfigV1)
```



## Config77 Objects

```python
class Config77(BaseModel)
```



## ClientAccess12 Objects

```python
class ClientAccess12(BaseModel)
```



## Auth20 Objects

```python
class Auth20(BaseModel)
```



## FrontConfigV1 Objects

```python
class FrontConfigV1(BaseModel)
```



## FrontNewConnectorRequestV1 Objects

```python
class FrontNewConnectorRequestV1(NewConnectorRequestV1, FrontConfigV1)
```



## Config78 Objects

```python
class Config78(BaseModel)
```



## FtpConfigV1 Objects

```python
class FtpConfigV1(BaseModel)
```



## FtpNewConnectorRequestV1 Objects

```python
class FtpNewConnectorRequestV1(NewConnectorRequestV1, FtpConfigV1)
```



## Config79 Objects

```python
class Config79(BaseModel)
```



## GainsightCustomerSuccessConfigV1 Objects

```python
class GainsightCustomerSuccessConfigV1(BaseModel)
```



## GainsightCustomerSuccessNewConnectorRequestV1 Objects

```python
class GainsightCustomerSuccessNewConnectorRequestV1(
        NewConnectorRequestV1, GainsightCustomerSuccessConfigV1)
```



## Config80 Objects

```python
class Config80(BaseModel)
```



## GcsConfigV1 Objects

```python
class GcsConfigV1(BaseModel)
```



## GcsNewConnectorRequestV1 Objects

```python
class GcsNewConnectorRequestV1(NewConnectorRequestV1, GcsConfigV1)
```



## Config81 Objects

```python
class Config81(BaseModel)
```



## GithubConfigV1 Objects

```python
class GithubConfigV1(BaseModel)
```



## GithubNewConnectorRequestV1 Objects

```python
class GithubNewConnectorRequestV1(NewConnectorRequestV1, GithubConfigV1)
```



## Report Objects

```python
class Report(BaseModel)
```



## Config82 Objects

```python
class Config82(BaseModel)
```



## ClientAccess13 Objects

```python
class ClientAccess13(BaseModel)
```



## Auth21 Objects

```python
class Auth21(BaseModel)
```



## GoogleAdsConfigV1 Objects

```python
class GoogleAdsConfigV1(BaseModel)
```



## GoogleAdsNewConnectorRequestV1 Objects

```python
class GoogleAdsNewConnectorRequestV1(NewConnectorRequestV1, GoogleAdsConfigV1)
```



## Report1 Objects

```python
class Report1(BaseModel)
```



## Config83 Objects

```python
class Config83(BaseModel)
```



## ClientAccess14 Objects

```python
class ClientAccess14(BaseModel)
```



## Auth22 Objects

```python
class Auth22(BaseModel)
```



## GoogleAnalyticsConfigV1 Objects

```python
class GoogleAnalyticsConfigV1(BaseModel)
```



## GoogleAnalyticsNewConnectorRequestV1 Objects

```python
class GoogleAnalyticsNewConnectorRequestV1(NewConnectorRequestV1,
                                           GoogleAnalyticsConfigV1)
```



## Config84 Objects

```python
class Config84(BaseModel)
```



## GoogleAnalytics360ConfigV1 Objects

```python
class GoogleAnalytics360ConfigV1(BaseModel)
```



## GoogleAnalytics360NewConnectorRequestV1 Objects

```python
class GoogleAnalytics360NewConnectorRequestV1(NewConnectorRequestV1,
                                              GoogleAnalytics360ConfigV1)
```



## Report2 Objects

```python
class Report2(BaseModel)
```



## Config85 Objects

```python
class Config85(BaseModel)
```



## ClientAccess15 Objects

```python
class ClientAccess15(BaseModel)
```



## Auth23 Objects

```python
class Auth23(BaseModel)
```



## GoogleAnalytics4ConfigV1 Objects

```python
class GoogleAnalytics4ConfigV1(BaseModel)
```



## GoogleAnalytics4NewConnectorRequestV1 Objects

```python
class GoogleAnalytics4NewConnectorRequestV1(NewConnectorRequestV1,
                                            GoogleAnalytics4ConfigV1)
```



## Config86 Objects

```python
class Config86(BaseModel)
```



## GoogleAnalytics4ExportConfigV1 Objects

```python
class GoogleAnalytics4ExportConfigV1(BaseModel)
```



## GoogleAnalytics4ExportNewConnectorRequestV1 Objects

```python
class GoogleAnalytics4ExportNewConnectorRequestV1(
        NewConnectorRequestV1, GoogleAnalytics4ExportConfigV1)
```



## Config87 Objects

```python
class Config87(BaseModel)
```



## ClientAccess16 Objects

```python
class ClientAccess16(BaseModel)
```



## Auth24 Objects

```python
class Auth24(BaseModel)
```



## GoogleAnalyticsMcfConfigV1 Objects

```python
class GoogleAnalyticsMcfConfigV1(BaseModel)
```



## GoogleAnalyticsMcfNewConnectorRequestV1 Objects

```python
class GoogleAnalyticsMcfNewConnectorRequestV1(NewConnectorRequestV1,
                                              GoogleAnalyticsMcfConfigV1)
```



## SecretsListItem2 Objects

```python
class SecretsListItem2(BaseModel)
```



## Config88 Objects

```python
class Config88(BaseModel)
```



## GoogleCloudFunctionConfigV1 Objects

```python
class GoogleCloudFunctionConfigV1(BaseModel)
```



## GoogleCloudFunctionNewConnectorRequestV1 Objects

```python
class GoogleCloudFunctionNewConnectorRequestV1(NewConnectorRequestV1,
                                               GoogleCloudFunctionConfigV1)
```



## Config89 Objects

```python
class Config89(BaseModel)
```



## GoogleCloudMysqlConfigV1 Objects

```python
class GoogleCloudMysqlConfigV1(BaseModel)
```



## GoogleCloudMysqlNewConnectorRequestV1 Objects

```python
class GoogleCloudMysqlNewConnectorRequestV1(NewConnectorRequestV1,
                                            GoogleCloudMysqlConfigV1)
```



## Config90 Objects

```python
class Config90(BaseModel)
```



## GoogleCloudPostgresqlConfigV1 Objects

```python
class GoogleCloudPostgresqlConfigV1(BaseModel)
```



## GoogleCloudPostgresqlNewConnectorRequestV1 Objects

```python
class GoogleCloudPostgresqlNewConnectorRequestV1(NewConnectorRequestV1,
                                                 GoogleCloudPostgresqlConfigV1
                                                 )
```



## Config91 Objects

```python
class Config91(BaseModel)
```



## Auth25 Objects

```python
class Auth25(BaseModel)
```



## GoogleCloudSqlserverConfigV1 Objects

```python
class GoogleCloudSqlserverConfigV1(BaseModel)
```



## GoogleCloudSqlserverNewConnectorRequestV1 Objects

```python
class GoogleCloudSqlserverNewConnectorRequestV1(NewConnectorRequestV1,
                                                GoogleCloudSqlserverConfigV1)
```



## Config92 Objects

```python
class Config92(BaseModel)
```



## Auth26 Objects

```python
class Auth26(BaseModel)
```



## GoogleDisplayAndVideo360ConfigV1 Objects

```python
class GoogleDisplayAndVideo360ConfigV1(BaseModel)
```



## GoogleDisplayAndVideo360NewConnectorRequestV1 Objects

```python
class GoogleDisplayAndVideo360NewConnectorRequestV1(
        NewConnectorRequestV1, GoogleDisplayAndVideo360ConfigV1)
```



## Config93 Objects

```python
class Config93(BaseModel)
```



## Auth27 Objects

```python
class Auth27(BaseModel)
```



## GoogleDriveConfigV1 Objects

```python
class GoogleDriveConfigV1(BaseModel)
```



## GoogleDriveNewConnectorRequestV1 Objects

```python
class GoogleDriveNewConnectorRequestV1(NewConnectorRequestV1,
                                       GoogleDriveConfigV1)
```



## Config94 Objects

```python
class Config94(BaseModel)
```



## ClientAccess17 Objects

```python
class ClientAccess17(BaseModel)
```



## Auth28 Objects

```python
class Auth28(BaseModel)
```



## GooglePlayConfigV1 Objects

```python
class GooglePlayConfigV1(BaseModel)
```



## GooglePlayNewConnectorRequestV1 Objects

```python
class GooglePlayNewConnectorRequestV1(NewConnectorRequestV1,
                                      GooglePlayConfigV1)
```



## Report3 Objects

```python
class Report3(BaseModel)
```



## Config95 Objects

```python
class Config95(BaseModel)
```



## ClientAccess18 Objects

```python
class ClientAccess18(BaseModel)
```



## Auth29 Objects

```python
class Auth29(BaseModel)
```



## GoogleSearchConsoleConfigV1 Objects

```python
class GoogleSearchConsoleConfigV1(BaseModel)
```



## GoogleSearchConsoleNewConnectorRequestV1 Objects

```python
class GoogleSearchConsoleNewConnectorRequestV1(NewConnectorRequestV1,
                                               GoogleSearchConsoleConfigV1)
```



## Config96 Objects

```python
class Config96(BaseModel)
```



## ClientAccess19 Objects

```python
class ClientAccess19(BaseModel)
```



## Auth30 Objects

```python
class Auth30(BaseModel)
```



## GoogleSheetsConfigV1 Objects

```python
class GoogleSheetsConfigV1(BaseModel)
```



## GoogleSheetsNewConnectorRequestV1 Objects

```python
class GoogleSheetsNewConnectorRequestV1(NewConnectorRequestV1,
                                        GoogleSheetsConfigV1)
```



## Config97 Objects

```python
class Config97(BaseModel)
```



## GreenhouseConfigV1 Objects

```python
class GreenhouseConfigV1(BaseModel)
```



## GreenhouseNewConnectorRequestV1 Objects

```python
class GreenhouseNewConnectorRequestV1(NewConnectorRequestV1,
                                      GreenhouseConfigV1)
```



## Config98 Objects

```python
class Config98(BaseModel)
```



## HeapConfigV1 Objects

```python
class HeapConfigV1(BaseModel)
```



## HeapNewConnectorRequestV1 Objects

```python
class HeapNewConnectorRequestV1(NewConnectorRequestV1, HeapConfigV1)
```



## Config99 Objects

```python
class Config99(BaseModel)
```



## Auth31 Objects

```python
class Auth31(BaseModel)
```



## HeightConfigV1 Objects

```python
class HeightConfigV1(BaseModel)
```



## HeightNewConnectorRequestV1 Objects

```python
class HeightNewConnectorRequestV1(NewConnectorRequestV1, HeightConfigV1)
```



## Config100 Objects

```python
class Config100(BaseModel)
```



## ClientAccess20 Objects

```python
class ClientAccess20(BaseModel)
```



## Auth32 Objects

```python
class Auth32(BaseModel)
```



## HelpscoutConfigV1 Objects

```python
class HelpscoutConfigV1(BaseModel)
```



## HelpscoutNewConnectorRequestV1 Objects

```python
class HelpscoutNewConnectorRequestV1(NewConnectorRequestV1, HelpscoutConfigV1)
```



## Config101 Objects

```python
class Config101(BaseModel)
```



## HerokuKafkaConfigV1 Objects

```python
class HerokuKafkaConfigV1(BaseModel)
```



## HerokuKafkaNewConnectorRequestV1 Objects

```python
class HerokuKafkaNewConnectorRequestV1(NewConnectorRequestV1,
                                       HerokuKafkaConfigV1)
```



## Config102 Objects

```python
class Config102(BaseModel)
```



## HerokuPostgresConfigV1 Objects

```python
class HerokuPostgresConfigV1(BaseModel)
```



## HerokuPostgresNewConnectorRequestV1 Objects

```python
class HerokuPostgresNewConnectorRequestV1(NewConnectorRequestV1,
                                          HerokuPostgresConfigV1)
```



## Config103 Objects

```python
class Config103(BaseModel)
```



## ClientAccess21 Objects

```python
class ClientAccess21(BaseModel)
```



## Auth33 Objects

```python
class Auth33(BaseModel)
```



## HubspotConfigV1 Objects

```python
class HubspotConfigV1(BaseModel)
```



## HubspotNewConnectorRequestV1 Objects

```python
class HubspotNewConnectorRequestV1(NewConnectorRequestV1, HubspotConfigV1)
```



## Config104 Objects

```python
class Config104(BaseModel)
```



## ClientAccess22 Objects

```python
class ClientAccess22(BaseModel)
```



## Auth34 Objects

```python
class Auth34(BaseModel)
```



## InstagramBusinessConfigV1 Objects

```python
class InstagramBusinessConfigV1(BaseModel)
```



## InstagramBusinessNewConnectorRequestV1 Objects

```python
class InstagramBusinessNewConnectorRequestV1(NewConnectorRequestV1,
                                             InstagramBusinessConfigV1)
```



## Config105 Objects

```python
class Config105(BaseModel)
```



## IntercomConfigV1 Objects

```python
class IntercomConfigV1(BaseModel)
```



## IntercomNewConnectorRequestV1 Objects

```python
class IntercomNewConnectorRequestV1(NewConnectorRequestV1, IntercomConfigV1)
```



## Config106 Objects

```python
class Config106(BaseModel)
```



## IterableConfigV1 Objects

```python
class IterableConfigV1(BaseModel)
```



## IterableNewConnectorRequestV1 Objects

```python
class IterableNewConnectorRequestV1(NewConnectorRequestV1, IterableConfigV1)
```



## Config107 Objects

```python
class Config107(BaseModel)
```



## ItunesConnectConfigV1 Objects

```python
class ItunesConnectConfigV1(BaseModel)
```



## ItunesConnectNewConnectorRequestV1 Objects

```python
class ItunesConnectNewConnectorRequestV1(NewConnectorRequestV1,
                                         ItunesConnectConfigV1)
```



## Config108 Objects

```python
class Config108(BaseModel)
```



## JiraConfigV1 Objects

```python
class JiraConfigV1(BaseModel)
```



## JiraNewConnectorRequestV1 Objects

```python
class JiraNewConnectorRequestV1(NewConnectorRequestV1, JiraConfigV1)
```



## Config109 Objects

```python
class Config109(BaseModel)
```



## KinesisConfigV1 Objects

```python
class KinesisConfigV1(BaseModel)
```



## KinesisNewConnectorRequestV1 Objects

```python
class KinesisNewConnectorRequestV1(NewConnectorRequestV1, KinesisConfigV1)
```



## Config110 Objects

```python
class Config110(BaseModel)
```



## KlaviyoConfigV1 Objects

```python
class KlaviyoConfigV1(BaseModel)
```



## KlaviyoNewConnectorRequestV1 Objects

```python
class KlaviyoNewConnectorRequestV1(NewConnectorRequestV1, KlaviyoConfigV1)
```



## Config111 Objects

```python
class Config111(BaseModel)
```



## KustomerConfigV1 Objects

```python
class KustomerConfigV1(BaseModel)
```



## KustomerNewConnectorRequestV1 Objects

```python
class KustomerNewConnectorRequestV1(NewConnectorRequestV1, KustomerConfigV1)
```



## Config112 Objects

```python
class Config112(BaseModel)
```



## LeverConfigV1 Objects

```python
class LeverConfigV1(BaseModel)
```



## LeverNewConnectorRequestV1 Objects

```python
class LeverNewConnectorRequestV1(NewConnectorRequestV1, LeverConfigV1)
```



## Config113 Objects

```python
class Config113(BaseModel)
```



## LightSpeedRetailConfigV1 Objects

```python
class LightSpeedRetailConfigV1(BaseModel)
```



## LightSpeedRetailNewConnectorRequestV1 Objects

```python
class LightSpeedRetailNewConnectorRequestV1(NewConnectorRequestV1,
                                            LightSpeedRetailConfigV1)
```



## Config114 Objects

```python
class Config114(BaseModel)
```



## ClientAccess23 Objects

```python
class ClientAccess23(BaseModel)
```



## Auth35 Objects

```python
class Auth35(BaseModel)
```



## LinkedinAdsConfigV1 Objects

```python
class LinkedinAdsConfigV1(BaseModel)
```



## LinkedinAdsNewConnectorRequestV1 Objects

```python
class LinkedinAdsNewConnectorRequestV1(NewConnectorRequestV1,
                                       LinkedinAdsConfigV1)
```



## Config115 Objects

```python
class Config115(BaseModel)
```



## ClientAccess24 Objects

```python
class ClientAccess24(BaseModel)
```



## Auth36 Objects

```python
class Auth36(BaseModel)
```



## LinkedinCompanyPagesConfigV1 Objects

```python
class LinkedinCompanyPagesConfigV1(BaseModel)
```



## LinkedinCompanyPagesNewConnectorRequestV1 Objects

```python
class LinkedinCompanyPagesNewConnectorRequestV1(NewConnectorRequestV1,
                                                LinkedinCompanyPagesConfigV1)
```



## Config116 Objects

```python
class Config116(BaseModel)
```



## MagentoMysqlConfigV1 Objects

```python
class MagentoMysqlConfigV1(BaseModel)
```



## MagentoMysqlNewConnectorRequestV1 Objects

```python
class MagentoMysqlNewConnectorRequestV1(NewConnectorRequestV1,
                                        MagentoMysqlConfigV1)
```



## Config117 Objects

```python
class Config117(BaseModel)
```



## MagentoMysqlRdsConfigV1 Objects

```python
class MagentoMysqlRdsConfigV1(BaseModel)
```



## MagentoMysqlRdsNewConnectorRequestV1 Objects

```python
class MagentoMysqlRdsNewConnectorRequestV1(NewConnectorRequestV1,
                                           MagentoMysqlRdsConfigV1)
```



## Config118 Objects

```python
class Config118(BaseModel)
```



## MailchimpConfigV1 Objects

```python
class MailchimpConfigV1(BaseModel)
```



## MailchimpNewConnectorRequestV1 Objects

```python
class MailchimpNewConnectorRequestV1(NewConnectorRequestV1, MailchimpConfigV1)
```



## Config119 Objects

```python
class Config119(BaseModel)
```



## MandrillConfigV1 Objects

```python
class MandrillConfigV1(BaseModel)
```



## MandrillNewConnectorRequestV1 Objects

```python
class MandrillNewConnectorRequestV1(NewConnectorRequestV1, MandrillConfigV1)
```



## Config120 Objects

```python
class Config120(BaseModel)
```



## MariaConfigV1 Objects

```python
class MariaConfigV1(BaseModel)
```



## MariaNewConnectorRequestV1 Objects

```python
class MariaNewConnectorRequestV1(NewConnectorRequestV1, MariaConfigV1)
```



## Config121 Objects

```python
class Config121(BaseModel)
```



## MariaAzureConfigV1 Objects

```python
class MariaAzureConfigV1(BaseModel)
```



## MariaAzureNewConnectorRequestV1 Objects

```python
class MariaAzureNewConnectorRequestV1(NewConnectorRequestV1,
                                      MariaAzureConfigV1)
```



## Config122 Objects

```python
class Config122(BaseModel)
```



## MariaRdsConfigV1 Objects

```python
class MariaRdsConfigV1(BaseModel)
```



## MariaRdsNewConnectorRequestV1 Objects

```python
class MariaRdsNewConnectorRequestV1(NewConnectorRequestV1, MariaRdsConfigV1)
```



## Config123 Objects

```python
class Config123(BaseModel)
```



## MarinConfigV1 Objects

```python
class MarinConfigV1(BaseModel)
```



## MarinNewConnectorRequestV1 Objects

```python
class MarinNewConnectorRequestV1(NewConnectorRequestV1, MarinConfigV1)
```



## Config124 Objects

```python
class Config124(BaseModel)
```



## MarketoConfigV1 Objects

```python
class MarketoConfigV1(BaseModel)
```



## MarketoNewConnectorRequestV1 Objects

```python
class MarketoNewConnectorRequestV1(NewConnectorRequestV1, MarketoConfigV1)
```



## Config125 Objects

```python
class Config125(BaseModel)
```



## MavenlinkConfigV1 Objects

```python
class MavenlinkConfigV1(BaseModel)
```



## MavenlinkNewConnectorRequestV1 Objects

```python
class MavenlinkNewConnectorRequestV1(NewConnectorRequestV1, MavenlinkConfigV1)
```



## Config126 Objects

```python
class Config126(BaseModel)
```



## Auth37 Objects

```python
class Auth37(BaseModel)
```



## MedalliaConfigV1 Objects

```python
class MedalliaConfigV1(BaseModel)
```



## MedalliaNewConnectorRequestV1 Objects

```python
class MedalliaNewConnectorRequestV1(NewConnectorRequestV1, MedalliaConfigV1)
```



## Config127 Objects

```python
class Config127(BaseModel)
```



## ClientAccess25 Objects

```python
class ClientAccess25(BaseModel)
```



## Auth38 Objects

```python
class Auth38(BaseModel)
```



## MicrosoftListsConfigV1 Objects

```python
class MicrosoftListsConfigV1(BaseModel)
```



## MicrosoftListsNewConnectorRequestV1 Objects

```python
class MicrosoftListsNewConnectorRequestV1(NewConnectorRequestV1,
                                          MicrosoftListsConfigV1)
```



## Config128 Objects

```python
class Config128(BaseModel)
```



## MixpanelConfigV1 Objects

```python
class MixpanelConfigV1(BaseModel)
```



## MixpanelNewConnectorRequestV1 Objects

```python
class MixpanelNewConnectorRequestV1(NewConnectorRequestV1, MixpanelConfigV1)
```



## Config129 Objects

```python
class Config129(BaseModel)
```



## MongoConfigV1 Objects

```python
class MongoConfigV1(BaseModel)
```



## MongoNewConnectorRequestV1 Objects

```python
class MongoNewConnectorRequestV1(NewConnectorRequestV1, MongoConfigV1)
```



## Config130 Objects

```python
class Config130(BaseModel)
```



## MongoShardedConfigV1 Objects

```python
class MongoShardedConfigV1(BaseModel)
```



## MongoShardedNewConnectorRequestV1 Objects

```python
class MongoShardedNewConnectorRequestV1(NewConnectorRequestV1,
                                        MongoShardedConfigV1)
```



## Config131 Objects

```python
class Config131(BaseModel)
```



## MysqlConfigV1 Objects

```python
class MysqlConfigV1(BaseModel)
```



## MysqlNewConnectorRequestV1 Objects

```python
class MysqlNewConnectorRequestV1(NewConnectorRequestV1, MysqlConfigV1)
```



## Config132 Objects

```python
class Config132(BaseModel)
```



## MysqlAzureConfigV1 Objects

```python
class MysqlAzureConfigV1(BaseModel)
```



## MysqlAzureNewConnectorRequestV1 Objects

```python
class MysqlAzureNewConnectorRequestV1(NewConnectorRequestV1,
                                      MysqlAzureConfigV1)
```



## Config133 Objects

```python
class Config133(BaseModel)
```



## MysqlRdsConfigV1 Objects

```python
class MysqlRdsConfigV1(BaseModel)
```



## MysqlRdsNewConnectorRequestV1 Objects

```python
class MysqlRdsNewConnectorRequestV1(NewConnectorRequestV1, MysqlRdsConfigV1)
```



## Config134 Objects

```python
class Config134(BaseModel)
```



## NetsuiteSuiteanalyticsConfigV1 Objects

```python
class NetsuiteSuiteanalyticsConfigV1(BaseModel)
```



## NetsuiteSuiteanalyticsNewConnectorRequestV1 Objects

```python
class NetsuiteSuiteanalyticsNewConnectorRequestV1(
        NewConnectorRequestV1, NetsuiteSuiteanalyticsConfigV1)
```



## Config135 Objects

```python
class Config135(BaseModel)
```



## ClientAccess26 Objects

```python
class ClientAccess26(BaseModel)
```



## Auth39 Objects

```python
class Auth39(BaseModel)
```



## OneDriveConfigV1 Objects

```python
class OneDriveConfigV1(BaseModel)
```



## OneDriveNewConnectorRequestV1 Objects

```python
class OneDriveNewConnectorRequestV1(NewConnectorRequestV1, OneDriveConfigV1)
```



## Config136 Objects

```python
class Config136(BaseModel)
```



## ClientAccess27 Objects

```python
class ClientAccess27(BaseModel)
```



## Auth40 Objects

```python
class Auth40(BaseModel)
```



## OptimizelyConfigV1 Objects

```python
class OptimizelyConfigV1(BaseModel)
```



## OptimizelyNewConnectorRequestV1 Objects

```python
class OptimizelyNewConnectorRequestV1(NewConnectorRequestV1,
                                      OptimizelyConfigV1)
```



## Config137 Objects

```python
class Config137(BaseModel)
```



## OracleConfigV1 Objects

```python
class OracleConfigV1(BaseModel)
```



## OracleNewConnectorRequestV1 Objects

```python
class OracleNewConnectorRequestV1(NewConnectorRequestV1, OracleConfigV1)
```



## Config138 Objects

```python
class Config138(BaseModel)
```



## OracleEbsConfigV1 Objects

```python
class OracleEbsConfigV1(BaseModel)
```



## OracleEbsNewConnectorRequestV1 Objects

```python
class OracleEbsNewConnectorRequestV1(NewConnectorRequestV1, OracleEbsConfigV1)
```



## Config139 Objects

```python
class Config139(BaseModel)
```



## OracleHvaConfigV1 Objects

```python
class OracleHvaConfigV1(BaseModel)
```



## OracleHvaNewConnectorRequestV1 Objects

```python
class OracleHvaNewConnectorRequestV1(NewConnectorRequestV1, OracleHvaConfigV1)
```



## Config140 Objects

```python
class Config140(BaseModel)
```



## OracleRacConfigV1 Objects

```python
class OracleRacConfigV1(BaseModel)
```



## OracleRacNewConnectorRequestV1 Objects

```python
class OracleRacNewConnectorRequestV1(NewConnectorRequestV1, OracleRacConfigV1)
```



## Config141 Objects

```python
class Config141(BaseModel)
```



## OracleRdsConfigV1 Objects

```python
class OracleRdsConfigV1(BaseModel)
```



## OracleRdsNewConnectorRequestV1 Objects

```python
class OracleRdsNewConnectorRequestV1(NewConnectorRequestV1, OracleRdsConfigV1)
```



## Config142 Objects

```python
class Config142(BaseModel)
```



## OutbrainConfigV1 Objects

```python
class OutbrainConfigV1(BaseModel)
```



## OutbrainNewConnectorRequestV1 Objects

```python
class OutbrainNewConnectorRequestV1(NewConnectorRequestV1, OutbrainConfigV1)
```



## Config143 Objects

```python
class Config143(BaseModel)
```



## Auth41 Objects

```python
class Auth41(BaseModel)
```



## OutreachConfigV1 Objects

```python
class OutreachConfigV1(BaseModel)
```



## OutreachNewConnectorRequestV1 Objects

```python
class OutreachNewConnectorRequestV1(NewConnectorRequestV1, OutreachConfigV1)
```



## Config144 Objects

```python
class Config144(BaseModel)
```



## PardotConfigV1 Objects

```python
class PardotConfigV1(BaseModel)
```



## PardotNewConnectorRequestV1 Objects

```python
class PardotNewConnectorRequestV1(NewConnectorRequestV1, PardotConfigV1)
```



## Config145 Objects

```python
class Config145(BaseModel)
```



## PaypalConfigV1 Objects

```python
class PaypalConfigV1(BaseModel)
```



## PaypalNewConnectorRequestV1 Objects

```python
class PaypalNewConnectorRequestV1(NewConnectorRequestV1, PaypalConfigV1)
```



## Config146 Objects

```python
class Config146(BaseModel)
```



## PaypalSandboxConfigV1 Objects

```python
class PaypalSandboxConfigV1(BaseModel)
```



## PaypalSandboxNewConnectorRequestV1 Objects

```python
class PaypalSandboxNewConnectorRequestV1(NewConnectorRequestV1,
                                         PaypalSandboxConfigV1)
```



## Config147 Objects

```python
class Config147(BaseModel)
```



## PendoConfigV1 Objects

```python
class PendoConfigV1(BaseModel)
```



## PendoNewConnectorRequestV1 Objects

```python
class PendoNewConnectorRequestV1(NewConnectorRequestV1, PendoConfigV1)
```



## Config148 Objects

```python
class Config148(BaseModel)
```



## ClientAccess28 Objects

```python
class ClientAccess28(BaseModel)
```



## Auth42 Objects

```python
class Auth42(BaseModel)
```



## PinterestAdsConfigV1 Objects

```python
class PinterestAdsConfigV1(BaseModel)
```



## PinterestAdsNewConnectorRequestV1 Objects

```python
class PinterestAdsNewConnectorRequestV1(NewConnectorRequestV1,
                                        PinterestAdsConfigV1)
```



## Config149 Objects

```python
class Config149(BaseModel)
```



## ClientAccess29 Objects

```python
class ClientAccess29(BaseModel)
```



## Auth43 Objects

```python
class Auth43(BaseModel)
```



## PipedriveConfigV1 Objects

```python
class PipedriveConfigV1(BaseModel)
```



## PipedriveNewConnectorRequestV1 Objects

```python
class PipedriveNewConnectorRequestV1(NewConnectorRequestV1, PipedriveConfigV1)
```



## Config150 Objects

```python
class Config150(BaseModel)
```



## PostgresConfigV1 Objects

```python
class PostgresConfigV1(BaseModel)
```



## PostgresNewConnectorRequestV1 Objects

```python
class PostgresNewConnectorRequestV1(NewConnectorRequestV1, PostgresConfigV1)
```



## Config151 Objects

```python
class Config151(BaseModel)
```



## PostgresRdsConfigV1 Objects

```python
class PostgresRdsConfigV1(BaseModel)
```



## PostgresRdsNewConnectorRequestV1 Objects

```python
class PostgresRdsNewConnectorRequestV1(NewConnectorRequestV1,
                                       PostgresRdsConfigV1)
```



## Config152 Objects

```python
class Config152(BaseModel)
```



## QualtricsConfigV1 Objects

```python
class QualtricsConfigV1(BaseModel)
```



## QualtricsNewConnectorRequestV1 Objects

```python
class QualtricsNewConnectorRequestV1(NewConnectorRequestV1, QualtricsConfigV1)
```



## Config153 Objects

```python
class Config153(BaseModel)
```



## ClientAccess30 Objects

```python
class ClientAccess30(BaseModel)
```



## Auth44 Objects

```python
class Auth44(BaseModel)
```



## QuickbooksConfigV1 Objects

```python
class QuickbooksConfigV1(BaseModel)
```



## QuickbooksNewConnectorRequestV1 Objects

```python
class QuickbooksNewConnectorRequestV1(NewConnectorRequestV1,
                                      QuickbooksConfigV1)
```



## Config154 Objects

```python
class Config154(BaseModel)
```



## RechargeConfigV1 Objects

```python
class RechargeConfigV1(BaseModel)
```



## RechargeNewConnectorRequestV1 Objects

```python
class RechargeNewConnectorRequestV1(NewConnectorRequestV1, RechargeConfigV1)
```



## Config155 Objects

```python
class Config155(BaseModel)
```



## RecurlyConfigV1 Objects

```python
class RecurlyConfigV1(BaseModel)
```



## RecurlyNewConnectorRequestV1 Objects

```python
class RecurlyNewConnectorRequestV1(NewConnectorRequestV1, RecurlyConfigV1)
```



## CustomReport Objects

```python
class CustomReport(BaseModel)
```



## Config156 Objects

```python
class Config156(BaseModel)
```



## ClientAccess31 Objects

```python
class ClientAccess31(BaseModel)
```



## Auth45 Objects

```python
class Auth45(BaseModel)
```



## RedditAdsConfigV1 Objects

```python
class RedditAdsConfigV1(BaseModel)
```



## RedditAdsNewConnectorRequestV1 Objects

```python
class RedditAdsNewConnectorRequestV1(NewConnectorRequestV1, RedditAdsConfigV1)
```



## Config157 Objects

```python
class Config157(BaseModel)
```



## S3ConfigV1 Objects

```python
class S3ConfigV1(BaseModel)
```



## S3NewConnectorRequestV1 Objects

```python
class S3NewConnectorRequestV1(NewConnectorRequestV1, S3ConfigV1)
```



## Config158 Objects

```python
class Config158(BaseModel)
```



## SageIntacctConfigV1 Objects

```python
class SageIntacctConfigV1(BaseModel)
```



## SageIntacctNewConnectorRequestV1 Objects

```python
class SageIntacctNewConnectorRequestV1(NewConnectorRequestV1,
                                       SageIntacctConfigV1)
```



## Config159 Objects

```python
class Config159(BaseModel)
```



## SailthruConfigV1 Objects

```python
class SailthruConfigV1(BaseModel)
```



## SailthruNewConnectorRequestV1 Objects

```python
class SailthruNewConnectorRequestV1(NewConnectorRequestV1, SailthruConfigV1)
```



## Config160 Objects

```python
class Config160(BaseModel)
```



## ClientAccess32 Objects

```python
class ClientAccess32(BaseModel)
```



## Auth46 Objects

```python
class Auth46(BaseModel)
```



## SalesforceConfigV1 Objects

```python
class SalesforceConfigV1(BaseModel)
```



## SalesforceNewConnectorRequestV1 Objects

```python
class SalesforceNewConnectorRequestV1(NewConnectorRequestV1,
                                      SalesforceConfigV1)
```



## Config161 Objects

```python
class Config161(BaseModel)
```



## SalesforceMarketingCloudConfigV1 Objects

```python
class SalesforceMarketingCloudConfigV1(BaseModel)
```



## SalesforceMarketingCloudNewConnectorRequestV1 Objects

```python
class SalesforceMarketingCloudNewConnectorRequestV1(
        NewConnectorRequestV1, SalesforceMarketingCloudConfigV1)
```



## Config162 Objects

```python
class Config162(BaseModel)
```



## ClientAccess33 Objects

```python
class ClientAccess33(BaseModel)
```



## Auth47 Objects

```python
class Auth47(BaseModel)
```



## SalesforceSandboxConfigV1 Objects

```python
class SalesforceSandboxConfigV1(BaseModel)
```



## SalesforceSandboxNewConnectorRequestV1 Objects

```python
class SalesforceSandboxNewConnectorRequestV1(NewConnectorRequestV1,
                                             SalesforceSandboxConfigV1)
```



## Config163 Objects

```python
class Config163(BaseModel)
```



## SapBusinessByDesignConfigV1 Objects

```python
class SapBusinessByDesignConfigV1(BaseModel)
```



## SapBusinessByDesignNewConnectorRequestV1 Objects

```python
class SapBusinessByDesignNewConnectorRequestV1(NewConnectorRequestV1,
                                               SapBusinessByDesignConfigV1)
```



## Config164 Objects

```python
class Config164(BaseModel)
```



## SegmentConfigV1 Objects

```python
class SegmentConfigV1(BaseModel)
```



## SegmentNewConnectorRequestV1 Objects

```python
class SegmentNewConnectorRequestV1(NewConnectorRequestV1, SegmentConfigV1)
```



## Config165 Objects

```python
class Config165(BaseModel)
```



## SendgridConfigV1 Objects

```python
class SendgridConfigV1(BaseModel)
```



## SendgridNewConnectorRequestV1 Objects

```python
class SendgridNewConnectorRequestV1(NewConnectorRequestV1, SendgridConfigV1)
```



## Config166 Objects

```python
class Config166(BaseModel)
```



## ServicenowConfigV1 Objects

```python
class ServicenowConfigV1(BaseModel)
```



## ServicenowNewConnectorRequestV1 Objects

```python
class ServicenowNewConnectorRequestV1(NewConnectorRequestV1,
                                      ServicenowConfigV1)
```



## Config167 Objects

```python
class Config167(BaseModel)
```



## SftpConfigV1 Objects

```python
class SftpConfigV1(BaseModel)
```



## SftpNewConnectorRequestV1 Objects

```python
class SftpNewConnectorRequestV1(NewConnectorRequestV1, SftpConfigV1)
```



## Config168 Objects

```python
class Config168(BaseModel)
```



## ClientAccess34 Objects

```python
class ClientAccess34(BaseModel)
```



## Auth48 Objects

```python
class Auth48(BaseModel)
```



## SharePointConfigV1 Objects

```python
class SharePointConfigV1(BaseModel)
```



## SharePointNewConnectorRequestV1 Objects

```python
class SharePointNewConnectorRequestV1(NewConnectorRequestV1,
                                      SharePointConfigV1)
```



## Config169 Objects

```python
class Config169(BaseModel)
```



## Auth49 Objects

```python
class Auth49(BaseModel)
```



## ShopifyConfigV1 Objects

```python
class ShopifyConfigV1(BaseModel)
```



## ShopifyNewConnectorRequestV1 Objects

```python
class ShopifyNewConnectorRequestV1(NewConnectorRequestV1, ShopifyConfigV1)
```



## Config170 Objects

```python
class Config170(BaseModel)
```



## ClientAccess35 Objects

```python
class ClientAccess35(BaseModel)
```



## Auth50 Objects

```python
class Auth50(BaseModel)
```



## SnapchatAdsConfigV1 Objects

```python
class SnapchatAdsConfigV1(BaseModel)
```



## SnapchatAdsNewConnectorRequestV1 Objects

```python
class SnapchatAdsNewConnectorRequestV1(NewConnectorRequestV1,
                                       SnapchatAdsConfigV1)
```



## Config171 Objects

```python
class Config171(BaseModel)
```



## SnowplowConfigV1 Objects

```python
class SnowplowConfigV1(BaseModel)
```



## SnowplowNewConnectorRequestV1 Objects

```python
class SnowplowNewConnectorRequestV1(NewConnectorRequestV1, SnowplowConfigV1)
```



## Config172 Objects

```python
class Config172(BaseModel)
```



## SplunkConfigV1 Objects

```python
class SplunkConfigV1(BaseModel)
```



## SplunkNewConnectorRequestV1 Objects

```python
class SplunkNewConnectorRequestV1(NewConnectorRequestV1, SplunkConfigV1)
```



## Config173 Objects

```python
class Config173(BaseModel)
```



## Auth51 Objects

```python
class Auth51(BaseModel)
```



## SqlServerConfigV1 Objects

```python
class SqlServerConfigV1(BaseModel)
```



## SqlServerNewConnectorRequestV1 Objects

```python
class SqlServerNewConnectorRequestV1(NewConnectorRequestV1, SqlServerConfigV1)
```



## Config174 Objects

```python
class Config174(BaseModel)
```



## Auth52 Objects

```python
class Auth52(BaseModel)
```



## SqlServerHvaConfigV1 Objects

```python
class SqlServerHvaConfigV1(BaseModel)
```



## SqlServerHvaNewConnectorRequestV1 Objects

```python
class SqlServerHvaNewConnectorRequestV1(NewConnectorRequestV1,
                                        SqlServerHvaConfigV1)
```



## Config175 Objects

```python
class Config175(BaseModel)
```



## Auth53 Objects

```python
class Auth53(BaseModel)
```



## SqlServerRdsConfigV1 Objects

```python
class SqlServerRdsConfigV1(BaseModel)
```



## SqlServerRdsNewConnectorRequestV1 Objects

```python
class SqlServerRdsNewConnectorRequestV1(NewConnectorRequestV1,
                                        SqlServerRdsConfigV1)
```



## Config176 Objects

```python
class Config176(BaseModel)
```



## SquareConfigV1 Objects

```python
class SquareConfigV1(BaseModel)
```



## SquareNewConnectorRequestV1 Objects

```python
class SquareNewConnectorRequestV1(NewConnectorRequestV1, SquareConfigV1)
```



## Config177 Objects

```python
class Config177(BaseModel)
```



## Auth54 Objects

```python
class Auth54(BaseModel)
```



## StripeConfigV1 Objects

```python
class StripeConfigV1(BaseModel)
```



## StripeNewConnectorRequestV1 Objects

```python
class StripeNewConnectorRequestV1(NewConnectorRequestV1, StripeConfigV1)
```



## Config178 Objects

```python
class Config178(BaseModel)
```



## Auth55 Objects

```python
class Auth55(BaseModel)
```



## StripeTestConfigV1 Objects

```python
class StripeTestConfigV1(BaseModel)
```



## StripeTestNewConnectorRequestV1 Objects

```python
class StripeTestNewConnectorRequestV1(NewConnectorRequestV1,
                                      StripeTestConfigV1)
```



## Config179 Objects

```python
class Config179(BaseModel)
```



## ClientAccess36 Objects

```python
class ClientAccess36(BaseModel)
```



## Auth56 Objects

```python
class Auth56(BaseModel)
```



## SurveyMonkeyConfigV1 Objects

```python
class SurveyMonkeyConfigV1(BaseModel)
```



## SurveyMonkeyNewConnectorRequestV1 Objects

```python
class SurveyMonkeyNewConnectorRequestV1(NewConnectorRequestV1,
                                        SurveyMonkeyConfigV1)
```



## Config180 Objects

```python
class Config180(BaseModel)
```



## TaboolaConfigV1 Objects

```python
class TaboolaConfigV1(BaseModel)
```



## TaboolaNewConnectorRequestV1 Objects

```python
class TaboolaNewConnectorRequestV1(NewConnectorRequestV1, TaboolaConfigV1)
```



## Config181 Objects

```python
class Config181(BaseModel)
```



## ClientAccess37 Objects

```python
class ClientAccess37(BaseModel)
```



## Auth57 Objects

```python
class Auth57(BaseModel)
```



## TiktokAdsConfigV1 Objects

```python
class TiktokAdsConfigV1(BaseModel)
```



## TiktokAdsNewConnectorRequestV1 Objects

```python
class TiktokAdsNewConnectorRequestV1(NewConnectorRequestV1, TiktokAdsConfigV1)
```



## Config182 Objects

```python
class Config182(BaseModel)
```



## TwilioConfigV1 Objects

```python
class TwilioConfigV1(BaseModel)
```



## TwilioNewConnectorRequestV1 Objects

```python
class TwilioNewConnectorRequestV1(NewConnectorRequestV1, TwilioConfigV1)
```



## Config183 Objects

```python
class Config183(BaseModel)
```



## ClientAccess38 Objects

```python
class ClientAccess38(BaseModel)
```



## Auth58 Objects

```python
class Auth58(BaseModel)
```



## TwitterConfigV1 Objects

```python
class TwitterConfigV1(BaseModel)
```



## TwitterNewConnectorRequestV1 Objects

```python
class TwitterNewConnectorRequestV1(NewConnectorRequestV1, TwitterConfigV1)
```



## Config184 Objects

```python
class Config184(BaseModel)
```



## ClientAccess39 Objects

```python
class ClientAccess39(BaseModel)
```



## Auth59 Objects

```python
class Auth59(BaseModel)
```



## TwitterAdsConfigV1 Objects

```python
class TwitterAdsConfigV1(BaseModel)
```



## TwitterAdsNewConnectorRequestV1 Objects

```python
class TwitterAdsNewConnectorRequestV1(NewConnectorRequestV1,
                                      TwitterAdsConfigV1)
```



## Config185 Objects

```python
class Config185(BaseModel)
```



## ClientAccess40 Objects

```python
class ClientAccess40(BaseModel)
```



## Auth60 Objects

```python
class Auth60(BaseModel)
```



## TypeformConfigV1 Objects

```python
class TypeformConfigV1(BaseModel)
```



## TypeformNewConnectorRequestV1 Objects

```python
class TypeformNewConnectorRequestV1(NewConnectorRequestV1, TypeformConfigV1)
```



## Config186 Objects

```python
class Config186(BaseModel)
```



## UservoiceConfigV1 Objects

```python
class UservoiceConfigV1(BaseModel)
```



## UservoiceNewConnectorRequestV1 Objects

```python
class UservoiceNewConnectorRequestV1(NewConnectorRequestV1, UservoiceConfigV1)
```



## Config187 Objects

```python
class Config187(BaseModel)
```



## WebhooksConfigV1 Objects

```python
class WebhooksConfigV1(BaseModel)
```



## WebhooksNewConnectorRequestV1 Objects

```python
class WebhooksNewConnectorRequestV1(NewConnectorRequestV1, WebhooksConfigV1)
```



## Config188 Objects

```python
class Config188(BaseModel)
```



## WoocommerceConfigV1 Objects

```python
class WoocommerceConfigV1(BaseModel)
```



## WoocommerceNewConnectorRequestV1 Objects

```python
class WoocommerceNewConnectorRequestV1(NewConnectorRequestV1,
                                       WoocommerceConfigV1)
```



## Config189 Objects

```python
class Config189(BaseModel)
```



## WorkdayConfigV1 Objects

```python
class WorkdayConfigV1(BaseModel)
```



## WorkdayNewConnectorRequestV1 Objects

```python
class WorkdayNewConnectorRequestV1(NewConnectorRequestV1, WorkdayConfigV1)
```



## Config190 Objects

```python
class Config190(BaseModel)
```



## WorkdayHcmConfigV1 Objects

```python
class WorkdayHcmConfigV1(BaseModel)
```



## WorkdayHcmNewConnectorRequestV1 Objects

```python
class WorkdayHcmNewConnectorRequestV1(NewConnectorRequestV1,
                                      WorkdayHcmConfigV1)
```



## Config191 Objects

```python
class Config191(BaseModel)
```



## XeroConfigV1 Objects

```python
class XeroConfigV1(BaseModel)
```



## XeroNewConnectorRequestV1 Objects

```python
class XeroNewConnectorRequestV1(NewConnectorRequestV1, XeroConfigV1)
```



## Config192 Objects

```python
class Config192(BaseModel)
```



## ClientAccess41 Objects

```python
class ClientAccess41(BaseModel)
```



## Auth61 Objects

```python
class Auth61(BaseModel)
```



## YahooGeminiConfigV1 Objects

```python
class YahooGeminiConfigV1(BaseModel)
```



## YahooGeminiNewConnectorRequestV1 Objects

```python
class YahooGeminiNewConnectorRequestV1(NewConnectorRequestV1,
                                       YahooGeminiConfigV1)
```



## Config193 Objects

```python
class Config193(BaseModel)
```



## ClientAccess42 Objects

```python
class ClientAccess42(BaseModel)
```



## Auth62 Objects

```python
class Auth62(BaseModel)
```



## YoutubeAnalyticsConfigV1 Objects

```python
class YoutubeAnalyticsConfigV1(BaseModel)
```



## YoutubeAnalyticsNewConnectorRequestV1 Objects

```python
class YoutubeAnalyticsNewConnectorRequestV1(NewConnectorRequestV1,
                                            YoutubeAnalyticsConfigV1)
```



## Config194 Objects

```python
class Config194(BaseModel)
```



## Auth63 Objects

```python
class Auth63(BaseModel)
```



## ZendeskConfigV1 Objects

```python
class ZendeskConfigV1(BaseModel)
```



## ZendeskNewConnectorRequestV1 Objects

```python
class ZendeskNewConnectorRequestV1(NewConnectorRequestV1, ZendeskConfigV1)
```



## Config195 Objects

```python
class Config195(BaseModel)
```



## Auth64 Objects

```python
class Auth64(BaseModel)
```



## ZendeskChatConfigV1 Objects

```python
class ZendeskChatConfigV1(BaseModel)
```



## ZendeskChatNewConnectorRequestV1 Objects

```python
class ZendeskChatNewConnectorRequestV1(NewConnectorRequestV1,
                                       ZendeskChatConfigV1)
```



## Config196 Objects

```python
class Config196(BaseModel)
```



## Auth65 Objects

```python
class Auth65(BaseModel)
```



## ZendeskSellConfigV1 Objects

```python
class ZendeskSellConfigV1(BaseModel)
```



## ZendeskSellNewConnectorRequestV1 Objects

```python
class ZendeskSellNewConnectorRequestV1(NewConnectorRequestV1,
                                       ZendeskSellConfigV1)
```



## Config197 Objects

```python
class Config197(BaseModel)
```



## ZendeskSunshineConfigV1 Objects

```python
class ZendeskSunshineConfigV1(BaseModel)
```



## ZendeskSunshineNewConnectorRequestV1 Objects

```python
class ZendeskSunshineNewConnectorRequestV1(NewConnectorRequestV1,
                                           ZendeskSunshineConfigV1)
```



## Config198 Objects

```python
class Config198(BaseModel)
```



## ClientAccess43 Objects

```python
class ClientAccess43(BaseModel)
```



## Auth66 Objects

```python
class Auth66(BaseModel)
```



## ZohoCrmConfigV1 Objects

```python
class ZohoCrmConfigV1(BaseModel)
```



## ZohoCrmNewConnectorRequestV1 Objects

```python
class ZohoCrmNewConnectorRequestV1(NewConnectorRequestV1, ZohoCrmConfigV1)
```



## Config199 Objects

```python
class Config199(BaseModel)
```



## ZuoraConfigV1 Objects

```python
class ZuoraConfigV1(BaseModel)
```



## ZuoraNewConnectorRequestV1 Objects

```python
class ZuoraNewConnectorRequestV1(NewConnectorRequestV1, ZuoraConfigV1)
```



## Config200 Objects

```python
class Config200(BaseModel)
```



## ZuoraSandboxConfigV1 Objects

```python
class ZuoraSandboxConfigV1(BaseModel)
```



## ZuoraSandboxNewConnectorRequestV1 Objects

```python
class ZuoraSandboxNewConnectorRequestV1(NewConnectorRequestV1,
                                        ZuoraSandboxConfigV1)
```



## Data Objects

```python
class Data(BaseModel)
```



## V1TeamsTeamIdConnectorsGetResponse Objects

```python
class V1TeamsTeamIdConnectorsGetResponse(BaseModel)
```



## V1TeamsTeamIdConnectorsPostResponse Objects

```python
class V1TeamsTeamIdConnectorsPostResponse(BaseModel)
```



## V1TeamsTeamIdUsersUserIdGetResponse Objects

```python
class V1TeamsTeamIdUsersUserIdGetResponse(BaseModel)
```



## V1TeamsTeamIdUsersUserIdDeleteResponse Objects

```python
class V1TeamsTeamIdUsersUserIdDeleteResponse(BaseModel)
```



## V1TeamsTeamIdUsersUserIdPatchResponse Objects

```python
class V1TeamsTeamIdUsersUserIdPatchResponse(BaseModel)
```



## Data1 Objects

```python
class Data1(BaseModel)
```



## V1UsersGetResponse Objects

```python
class V1UsersGetResponse(BaseModel)
```



## V1UsersPostResponse Objects

```python
class V1UsersPostResponse(BaseModel)
```



## V1TeamsTeamIdGetResponse Objects

```python
class V1TeamsTeamIdGetResponse(BaseModel)
```



## V1TeamsTeamIdDeleteResponse Objects

```python
class V1TeamsTeamIdDeleteResponse(BaseModel)
```



## V1TeamsTeamIdPatchResponse Objects

```python
class V1TeamsTeamIdPatchResponse(BaseModel)
```



## V1TeamsTeamIdRoleDeleteResponse Objects

```python
class V1TeamsTeamIdRoleDeleteResponse(BaseModel)
```



## Data2 Objects

```python
class Data2(BaseModel)
```



## V1UsersUserIdGroupsGetResponse Objects

```python
class V1UsersUserIdGroupsGetResponse(BaseModel)
```



## V1UsersUserIdGroupsPostResponse Objects

```python
class V1UsersUserIdGroupsPostResponse(BaseModel)
```



## Data3 Objects

```python
class Data3(BaseModel)
```



## V1TeamsTeamIdGroupsGetResponse Objects

```python
class V1TeamsTeamIdGroupsGetResponse(BaseModel)
```



## V1TeamsTeamIdGroupsPostResponse Objects

```python
class V1TeamsTeamIdGroupsPostResponse(BaseModel)
```



## V1CertificatesPostResponse Objects

```python
class V1CertificatesPostResponse(BaseModel)
```



## V1DestinationsPostResponse Objects

```python
class V1DestinationsPostResponse(BaseModel)
```



## V1UsersIdDeleteResponse Objects

```python
class V1UsersIdDeleteResponse(BaseModel)
```



## V1UsersUserIdGetResponse Objects

```python
class V1UsersUserIdGetResponse(BaseModel)
```



## V1UsersUserIdPatchResponse Objects

```python
class V1UsersUserIdPatchResponse(BaseModel)
```



## V1GroupsGroupIdGetResponse Objects

```python
class V1GroupsGroupIdGetResponse(BaseModel)
```



## V1GroupsGroupIdDeleteResponse Objects

```python
class V1GroupsGroupIdDeleteResponse(BaseModel)
```



## V1GroupsGroupIdPatchResponse Objects

```python
class V1GroupsGroupIdPatchResponse(BaseModel)
```



## V1UsersUserIdConnectorsConnectorIdGetResponse Objects

```python
class V1UsersUserIdConnectorsConnectorIdGetResponse(BaseModel)
```



## V1UsersUserIdConnectorsConnectorIdDeleteResponse Objects

```python
class V1UsersUserIdConnectorsConnectorIdDeleteResponse(BaseModel)
```



## V1UsersUserIdConnectorsConnectorIdPatchResponse Objects

```python
class V1UsersUserIdConnectorsConnectorIdPatchResponse(BaseModel)
```



## V1ConnectorsConnectorIdConnectCardPostResponse Objects

```python
class V1ConnectorsConnectorIdConnectCardPostResponse(BaseModel)
```



## Data4 Objects

```python
class Data4(BaseModel)
```



## V1MetadataNameGetResponse Objects

```python
class V1MetadataNameGetResponse(BaseModel)
```



## V1DbtTransformationsTransformationIdGetResponse Objects

```python
class V1DbtTransformationsTransformationIdGetResponse(BaseModel)
```



## V1DbtTransformationsTransformationIdDeleteResponse Objects

```python
class V1DbtTransformationsTransformationIdDeleteResponse(BaseModel)
```



## V1DbtTransformationsTransformationIdPatchResponse Objects

```python
class V1DbtTransformationsTransformationIdPatchResponse(BaseModel)
```



## V1DbtProjectsProjectIdGetResponse Objects

```python
class V1DbtProjectsProjectIdGetResponse(BaseModel)
```



## V1TeamsTeamIdGroupsGroupIdGetResponse Objects

```python
class V1TeamsTeamIdGroupsGroupIdGetResponse(BaseModel)
```



## V1TeamsTeamIdGroupsGroupIdDeleteResponse Objects

```python
class V1TeamsTeamIdGroupsGroupIdDeleteResponse(BaseModel)
```



## V1TeamsTeamIdGroupsGroupIdPatchResponse Objects

```python
class V1TeamsTeamIdGroupsGroupIdPatchResponse(BaseModel)
```



## V1ConnectorsConnectorIdResyncPostResponse Objects

```python
class V1ConnectorsConnectorIdResyncPostResponse(BaseModel)
```



## V1UsersUserIdRoleDeleteResponse Objects

```python
class V1UsersUserIdRoleDeleteResponse(BaseModel)
```



## Data5 Objects

```python
class Data5(BaseModel)
```



## V1GroupsGroupIdUsersGetResponse Objects

```python
class V1GroupsGroupIdUsersGetResponse(BaseModel)
```



## V1GroupsGroupIdUsersPostResponse Objects

```python
class V1GroupsGroupIdUsersPostResponse(BaseModel)
```



## V1ConnectorsConnectorIdSchemasTablesResyncPostRequest Objects

```python
class V1ConnectorsConnectorIdSchemasTablesResyncPostRequest(BaseModel)
```



### Config Objects

```python
class Config()
```



## V1ConnectorsConnectorIdSchemasTablesResyncPostResponse Objects

```python
class V1ConnectorsConnectorIdSchemasTablesResyncPostResponse(BaseModel)
```



## V1DestinationsDestinationIdTestPostResponse Objects

```python
class V1DestinationsDestinationIdTestPostResponse(BaseModel)
```



## Data6 Objects

```python
class Data6(BaseModel)
```



## V1MetadataConnectorsConnectorIdSchemasGetResponse Objects

```python
class V1MetadataConnectorsConnectorIdSchemasGetResponse(BaseModel)
```



## Data7 Objects

```python
class Data7(BaseModel)
```



## V1GroupsGetResponse Objects

```python
class V1GroupsGetResponse(BaseModel)
```



## V1GroupsPostResponse Objects

```python
class V1GroupsPostResponse(BaseModel)
```



## V1FingerprintsPostResponse Objects

```python
class V1FingerprintsPostResponse(BaseModel)
```



## V1ConnectorsConnectorIdDeleteResponse Objects

```python
class V1ConnectorsConnectorIdDeleteResponse(BaseModel)
```



## V1MetadataNameServiceGetResponse Objects

```python
class V1MetadataNameServiceGetResponse(BaseModel)
```



## Data8 Objects

```python
class Data8(BaseModel)
```



## V1TeamsGetResponse Objects

```python
class V1TeamsGetResponse(BaseModel)
```



## V1TeamsPostResponse Objects

```python
class V1TeamsPostResponse(BaseModel)
```



## V1DbtProjectsProjectIdTestPostResponse Objects

```python
class V1DbtProjectsProjectIdTestPostResponse(BaseModel)
```



## V1ConnectorsConnectorIdSyncPostResponse Objects

```python
class V1ConnectorsConnectorIdSyncPostResponse(BaseModel)
```



## V1GroupsGroupIdUsersUserIdDeleteResponse Objects

```python
class V1GroupsGroupIdUsersUserIdDeleteResponse(BaseModel)
```



## Data9 Objects

```python
class Data9(BaseModel)
```



## V1MetadataConnectorsConnectorIdColumnsGetResponse Objects

```python
class V1MetadataConnectorsConnectorIdColumnsGetResponse(BaseModel)
```



## Data10 Objects

```python
class Data10(BaseModel)
```



## V1MetadataConnectorsConnectorIdTablesGetResponse Objects

```python
class V1MetadataConnectorsConnectorIdTablesGetResponse(BaseModel)
```



## Data11 Objects

```python
class Data11(BaseModel)
```



## V1DbtProjectsProjectIdTransformationsGetResponse Objects

```python
class V1DbtProjectsProjectIdTransformationsGetResponse(BaseModel)
```



## V1DbtProjectsProjectIdTransformationsPostResponse Objects

```python
class V1DbtProjectsProjectIdTransformationsPostResponse(BaseModel)
```



## Data12 Objects

```python
class Data12(BaseModel)
```



## V1DbtProjectsGetResponse Objects

```python
class V1DbtProjectsGetResponse(BaseModel)
```



## V1DbtProjectsPostResponse Objects

```python
class V1DbtProjectsPostResponse(BaseModel)
```



## Data13 Objects

```python
class Data13(BaseModel)
```



## V1RolesGetResponse Objects

```python
class V1RolesGetResponse(BaseModel)
```



## Data14 Objects

```python
class Data14(BaseModel)
```



## V1DbtProjectsProjectIdModelsGetResponse Objects

```python
class V1DbtProjectsProjectIdModelsGetResponse(BaseModel)
```



## V1TeamsTeamIdConnectorsConnectorIdGetResponse Objects

```python
class V1TeamsTeamIdConnectorsConnectorIdGetResponse(BaseModel)
```



## V1TeamsTeamIdConnectorsConnectorIdDeleteResponse Objects

```python
class V1TeamsTeamIdConnectorsConnectorIdDeleteResponse(BaseModel)
```



## V1TeamsTeamIdConnectorsConnectorIdPatchResponse Objects

```python
class V1TeamsTeamIdConnectorsConnectorIdPatchResponse(BaseModel)
```



## Data15 Objects

```python
class Data15(BaseModel)
```



## V1GroupsGroupIdConnectorsGetResponse Objects

```python
class V1GroupsGroupIdConnectorsGetResponse(BaseModel)
```



## V1DestinationsDestinationIdGetResponse Objects

```python
class V1DestinationsDestinationIdGetResponse(BaseModel)
```



## V1DestinationsDestinationIdDeleteResponse Objects

```python
class V1DestinationsDestinationIdDeleteResponse(BaseModel)
```



## V1DestinationsDestinationIdPatchResponse Objects

```python
class V1DestinationsDestinationIdPatchResponse(BaseModel)
```



## V1WebhooksGetResponse Objects

```python
class V1WebhooksGetResponse(BaseModel)
```



## Data16 Objects

```python
class Data16(BaseModel)
```



## V1TeamsTeamIdUsersGetResponse Objects

```python
class V1TeamsTeamIdUsersGetResponse(BaseModel)
```



## V1TeamsTeamIdUsersPostResponse Objects

```python
class V1TeamsTeamIdUsersPostResponse(BaseModel)
```



## V1UsersUserIdGroupsGroupIdGetResponse Objects

```python
class V1UsersUserIdGroupsGroupIdGetResponse(BaseModel)
```



## V1UsersUserIdGroupsGroupIdDeleteResponse Objects

```python
class V1UsersUserIdGroupsGroupIdDeleteResponse(BaseModel)
```



## V1UsersUserIdGroupsGroupIdPatchResponse Objects

```python
class V1UsersUserIdGroupsGroupIdPatchResponse(BaseModel)
```



## Data17 Objects

```python
class Data17(BaseModel)
```



## V1UsersUserIdConnectorsGetResponse Objects

```python
class V1UsersUserIdConnectorsGetResponse(BaseModel)
```



## V1DbtModelsModelIdGetResponse Objects

```python
class V1DbtModelsModelIdGetResponse(BaseModel)
```



## ConnectorResponseV1 Objects

```python
class ConnectorResponseV1(BaseModel)
```



## SchemaUpdateRequest Objects

```python
class SchemaUpdateRequest(BaseModel)
```



## StandardConfigUpdateRequest Objects

```python
class StandardConfigUpdateRequest(BaseModel)
```



## ColumnConfigResponse Objects

```python
class ColumnConfigResponse(BaseModel)
```



## TableConfigResponse Objects

```python
class TableConfigResponse(BaseModel)
```



## TableColumnsConfigResponse Objects

```python
class TableColumnsConfigResponse(BaseModel)
```



## NewTransformationRequest Objects

```python
class NewTransformationRequest(BaseModel)
```



## ActivecampaignConnectorResponseV1 Objects

```python
class ActivecampaignConnectorResponseV1(ConnectorResponseV1,
                                        ActivecampaignConfigV1)
```



## AdjustConnectorResponseV1 Objects

```python
class AdjustConnectorResponseV1(ConnectorResponseV1, AdjustConfigV1)
```



## AdobeAnalyticsConnectorResponseV1 Objects

```python
class AdobeAnalyticsConnectorResponseV1(ConnectorResponseV1,
                                        AdobeAnalyticsConfigV1)
```



## AdobeAnalyticsDataFeedConnectorResponseV1 Objects

```python
class AdobeAnalyticsDataFeedConnectorResponseV1(ConnectorResponseV1,
                                                AdobeAnalyticsDataFeedConfigV1
                                                )
```



## AdpWorkforceNowConnectorResponseV1 Objects

```python
class AdpWorkforceNowConnectorResponseV1(ConnectorResponseV1,
                                         AdpWorkforceNowConfigV1)
```



## AdrollConnectorResponseV1 Objects

```python
class AdrollConnectorResponseV1(ConnectorResponseV1, AdrollConfigV1)
```



## AirtableConnectorResponseV1 Objects

```python
class AirtableConnectorResponseV1(ConnectorResponseV1, AirtableConfigV1)
```



## AmazonAdsConnectorResponseV1 Objects

```python
class AmazonAdsConnectorResponseV1(ConnectorResponseV1, AmazonAdsConfigV1)
```



## AmplitudeConnectorResponseV1 Objects

```python
class AmplitudeConnectorResponseV1(ConnectorResponseV1, AmplitudeConfigV1)
```



## AnaplanConnectorResponseV1 Objects

```python
class AnaplanConnectorResponseV1(ConnectorResponseV1, AnaplanConfigV1)
```



## ApacheKafkaConnectorResponseV1 Objects

```python
class ApacheKafkaConnectorResponseV1(ConnectorResponseV1, ApacheKafkaConfigV1)
```



## AppleSearchAdsConnectorResponseV1 Objects

```python
class AppleSearchAdsConnectorResponseV1(ConnectorResponseV1,
                                        AppleSearchAdsConfigV1)
```



## AppsflyerConnectorResponseV1 Objects

```python
class AppsflyerConnectorResponseV1(ConnectorResponseV1, AppsflyerConfigV1)
```



## AsanaConnectorResponseV1 Objects

```python
class AsanaConnectorResponseV1(ConnectorResponseV1, AsanaConfigV1)
```



## AuroraConnectorResponseV1 Objects

```python
class AuroraConnectorResponseV1(ConnectorResponseV1, AuroraConfigV1)
```



## AuroraPostgresConnectorResponseV1 Objects

```python
class AuroraPostgresConnectorResponseV1(ConnectorResponseV1,
                                        AuroraPostgresConfigV1)
```



## AwsCloudtrailConnectorResponseV1 Objects

```python
class AwsCloudtrailConnectorResponseV1(ConnectorResponseV1,
                                       AwsCloudtrailConfigV1)
```



## AwsInventoryConnectorResponseV1 Objects

```python
class AwsInventoryConnectorResponseV1(ConnectorResponseV1,
                                      AwsInventoryConfigV1)
```



## AwsLambdaConnectorResponseV1 Objects

```python
class AwsLambdaConnectorResponseV1(ConnectorResponseV1, AwsLambdaConfigV1)
```



## AwsMskConnectorResponseV1 Objects

```python
class AwsMskConnectorResponseV1(ConnectorResponseV1, AwsMskConfigV1)
```



## AzureBlobStorageConnectorResponseV1 Objects

```python
class AzureBlobStorageConnectorResponseV1(ConnectorResponseV1,
                                          AzureBlobStorageConfigV1)
```



## AzureEventHubConnectorResponseV1 Objects

```python
class AzureEventHubConnectorResponseV1(ConnectorResponseV1,
                                       AzureEventHubConfigV1)
```



## AzureFunctionConnectorResponseV1 Objects

```python
class AzureFunctionConnectorResponseV1(ConnectorResponseV1,
                                       AzureFunctionConfigV1)
```



## AzurePostgresConnectorResponseV1 Objects

```python
class AzurePostgresConnectorResponseV1(ConnectorResponseV1,
                                       AzurePostgresConfigV1)
```



## AzureServiceBusConnectorResponseV1 Objects

```python
class AzureServiceBusConnectorResponseV1(ConnectorResponseV1,
                                         AzureServiceBusConfigV1)
```



## AzureSqlDbConnectorResponseV1 Objects

```python
class AzureSqlDbConnectorResponseV1(ConnectorResponseV1, AzureSqlDbConfigV1)
```



## AzureSqlManagedDbConnectorResponseV1 Objects

```python
class AzureSqlManagedDbConnectorResponseV1(ConnectorResponseV1,
                                           AzureSqlManagedDbConfigV1)
```



## BingadsConnectorResponseV1 Objects

```python
class BingadsConnectorResponseV1(ConnectorResponseV1, BingadsConfigV1)
```



## BoxConnectorResponseV1 Objects

```python
class BoxConnectorResponseV1(ConnectorResponseV1, BoxConfigV1)
```



## BraintreeConnectorResponseV1 Objects

```python
class BraintreeConnectorResponseV1(ConnectorResponseV1, BraintreeConfigV1)
```



## BraintreeSandboxConnectorResponseV1 Objects

```python
class BraintreeSandboxConnectorResponseV1(ConnectorResponseV1,
                                          BraintreeSandboxConfigV1)
```



## BranchConnectorResponseV1 Objects

```python
class BranchConnectorResponseV1(ConnectorResponseV1, BranchConfigV1)
```



## BrazeConnectorResponseV1 Objects

```python
class BrazeConnectorResponseV1(ConnectorResponseV1, BrazeConfigV1)
```



## CloudfrontConnectorResponseV1 Objects

```python
class CloudfrontConnectorResponseV1(ConnectorResponseV1, CloudfrontConfigV1)
```



## ConcurConnectorResponseV1 Objects

```python
class ConcurConnectorResponseV1(ConnectorResponseV1, ConcurConfigV1)
```



## ConfluentCloudConnectorResponseV1 Objects

```python
class ConfluentCloudConnectorResponseV1(ConnectorResponseV1,
                                        ConfluentCloudConfigV1)
```



## CoupaConnectorResponseV1 Objects

```python
class CoupaConnectorResponseV1(ConnectorResponseV1, CoupaConfigV1)
```



## CriteoConnectorResponseV1 Objects

```python
class CriteoConnectorResponseV1(ConnectorResponseV1, CriteoConfigV1)
```



## DelightedConnectorResponseV1 Objects

```python
class DelightedConnectorResponseV1(ConnectorResponseV1, DelightedConfigV1)
```



## DocumentdbConnectorResponseV1 Objects

```python
class DocumentdbConnectorResponseV1(ConnectorResponseV1, DocumentdbConfigV1)
```



## DoubleClickCampaignManagerConnectorResponseV1 Objects

```python
class DoubleClickCampaignManagerConnectorResponseV1(
        ConnectorResponseV1, DoubleClickCampaignManagerConfigV1)
```



## DoubleClickPublishersConnectorResponseV1 Objects

```python
class DoubleClickPublishersConnectorResponseV1(ConnectorResponseV1,
                                               DoubleClickPublishersConfigV1)
```



## DriftConnectorResponseV1 Objects

```python
class DriftConnectorResponseV1(ConnectorResponseV1, DriftConfigV1)
```



## DropboxConnectorResponseV1 Objects

```python
class DropboxConnectorResponseV1(ConnectorResponseV1, DropboxConfigV1)
```



## Dynamics365ConnectorResponseV1 Objects

```python
class Dynamics365ConnectorResponseV1(ConnectorResponseV1, Dynamics365ConfigV1)
```



## Dynamics365FoConnectorResponseV1 Objects

```python
class Dynamics365FoConnectorResponseV1(ConnectorResponseV1,
                                       Dynamics365FoConfigV1)
```



## DynamodbConnectorResponseV1 Objects

```python
class DynamodbConnectorResponseV1(ConnectorResponseV1, DynamodbConfigV1)
```



## EloquaConnectorResponseV1 Objects

```python
class EloquaConnectorResponseV1(ConnectorResponseV1, EloquaConfigV1)
```



## EmailConnectorResponseV1 Objects

```python
class EmailConnectorResponseV1(ConnectorResponseV1, EmailConfigV1)
```



## FacebookConnectorResponseV1 Objects

```python
class FacebookConnectorResponseV1(ConnectorResponseV1, FacebookConfigV1)
```



## FacebookAdAccountConnectorResponseV1 Objects

```python
class FacebookAdAccountConnectorResponseV1(ConnectorResponseV1,
                                           FacebookAdAccountConfigV1)
```



## FacebookAdsConnectorResponseV1 Objects

```python
class FacebookAdsConnectorResponseV1(ConnectorResponseV1, FacebookAdsConfigV1)
```



## FacebookPagesConnectorResponseV1 Objects

```python
class FacebookPagesConnectorResponseV1(ConnectorResponseV1,
                                       FacebookPagesConfigV1)
```



## FinancialForceConnectorResponseV1 Objects

```python
class FinancialForceConnectorResponseV1(ConnectorResponseV1,
                                        FinancialForceConfigV1)
```



## FivetranLogConnectorResponseV1 Objects

```python
class FivetranLogConnectorResponseV1(ConnectorResponseV1, FivetranLogConfigV1)
```



## FreshdeskConnectorResponseV1 Objects

```python
class FreshdeskConnectorResponseV1(ConnectorResponseV1, FreshdeskConfigV1)
```



## FrontConnectorResponseV1 Objects

```python
class FrontConnectorResponseV1(ConnectorResponseV1, FrontConfigV1)
```



## FtpConnectorResponseV1 Objects

```python
class FtpConnectorResponseV1(ConnectorResponseV1, FtpConfigV1)
```



## GainsightCustomerSuccessConnectorResponseV1 Objects

```python
class GainsightCustomerSuccessConnectorResponseV1(
        ConnectorResponseV1, GainsightCustomerSuccessConfigV1)
```



## GcsConnectorResponseV1 Objects

```python
class GcsConnectorResponseV1(ConnectorResponseV1, GcsConfigV1)
```



## GithubConnectorResponseV1 Objects

```python
class GithubConnectorResponseV1(ConnectorResponseV1, GithubConfigV1)
```



## GoogleAdsConnectorResponseV1 Objects

```python
class GoogleAdsConnectorResponseV1(ConnectorResponseV1, GoogleAdsConfigV1)
```



## GoogleAnalyticsConnectorResponseV1 Objects

```python
class GoogleAnalyticsConnectorResponseV1(ConnectorResponseV1,
                                         GoogleAnalyticsConfigV1)
```



## GoogleAnalytics360ConnectorResponseV1 Objects

```python
class GoogleAnalytics360ConnectorResponseV1(ConnectorResponseV1,
                                            GoogleAnalytics360ConfigV1)
```



## GoogleAnalytics4ConnectorResponseV1 Objects

```python
class GoogleAnalytics4ConnectorResponseV1(ConnectorResponseV1,
                                          GoogleAnalytics4ConfigV1)
```



## GoogleAnalytics4ExportConnectorResponseV1 Objects

```python
class GoogleAnalytics4ExportConnectorResponseV1(ConnectorResponseV1,
                                                GoogleAnalytics4ExportConfigV1
                                                )
```



## GoogleAnalyticsMcfConnectorResponseV1 Objects

```python
class GoogleAnalyticsMcfConnectorResponseV1(ConnectorResponseV1,
                                            GoogleAnalyticsMcfConfigV1)
```



## GoogleCloudFunctionConnectorResponseV1 Objects

```python
class GoogleCloudFunctionConnectorResponseV1(ConnectorResponseV1,
                                             GoogleCloudFunctionConfigV1)
```



## GoogleCloudMysqlConnectorResponseV1 Objects

```python
class GoogleCloudMysqlConnectorResponseV1(ConnectorResponseV1,
                                          GoogleCloudMysqlConfigV1)
```



## GoogleCloudPostgresqlConnectorResponseV1 Objects

```python
class GoogleCloudPostgresqlConnectorResponseV1(ConnectorResponseV1,
                                               GoogleCloudPostgresqlConfigV1)
```



## GoogleCloudSqlserverConnectorResponseV1 Objects

```python
class GoogleCloudSqlserverConnectorResponseV1(ConnectorResponseV1,
                                              GoogleCloudSqlserverConfigV1)
```



## GoogleDisplayAndVideo360ConnectorResponseV1 Objects

```python
class GoogleDisplayAndVideo360ConnectorResponseV1(
        ConnectorResponseV1, GoogleDisplayAndVideo360ConfigV1)
```



## GoogleDriveConnectorResponseV1 Objects

```python
class GoogleDriveConnectorResponseV1(ConnectorResponseV1, GoogleDriveConfigV1)
```



## GooglePlayConnectorResponseV1 Objects

```python
class GooglePlayConnectorResponseV1(ConnectorResponseV1, GooglePlayConfigV1)
```



## GoogleSearchConsoleConnectorResponseV1 Objects

```python
class GoogleSearchConsoleConnectorResponseV1(ConnectorResponseV1,
                                             GoogleSearchConsoleConfigV1)
```



## GoogleSheetsConnectorResponseV1 Objects

```python
class GoogleSheetsConnectorResponseV1(ConnectorResponseV1,
                                      GoogleSheetsConfigV1)
```



## GreenhouseConnectorResponseV1 Objects

```python
class GreenhouseConnectorResponseV1(ConnectorResponseV1, GreenhouseConfigV1)
```



## HeapConnectorResponseV1 Objects

```python
class HeapConnectorResponseV1(ConnectorResponseV1, HeapConfigV1)
```



## HeightConnectorResponseV1 Objects

```python
class HeightConnectorResponseV1(ConnectorResponseV1, HeightConfigV1)
```



## HelpscoutConnectorResponseV1 Objects

```python
class HelpscoutConnectorResponseV1(ConnectorResponseV1, HelpscoutConfigV1)
```



## HerokuKafkaConnectorResponseV1 Objects

```python
class HerokuKafkaConnectorResponseV1(ConnectorResponseV1, HerokuKafkaConfigV1)
```



## HerokuPostgresConnectorResponseV1 Objects

```python
class HerokuPostgresConnectorResponseV1(ConnectorResponseV1,
                                        HerokuPostgresConfigV1)
```



## HubspotConnectorResponseV1 Objects

```python
class HubspotConnectorResponseV1(ConnectorResponseV1, HubspotConfigV1)
```



## InstagramBusinessConnectorResponseV1 Objects

```python
class InstagramBusinessConnectorResponseV1(ConnectorResponseV1,
                                           InstagramBusinessConfigV1)
```



## IntercomConnectorResponseV1 Objects

```python
class IntercomConnectorResponseV1(ConnectorResponseV1, IntercomConfigV1)
```



## IterableConnectorResponseV1 Objects

```python
class IterableConnectorResponseV1(ConnectorResponseV1, IterableConfigV1)
```



## ItunesConnectConnectorResponseV1 Objects

```python
class ItunesConnectConnectorResponseV1(ConnectorResponseV1,
                                       ItunesConnectConfigV1)
```



## JiraConnectorResponseV1 Objects

```python
class JiraConnectorResponseV1(ConnectorResponseV1, JiraConfigV1)
```



## KinesisConnectorResponseV1 Objects

```python
class KinesisConnectorResponseV1(ConnectorResponseV1, KinesisConfigV1)
```



## KlaviyoConnectorResponseV1 Objects

```python
class KlaviyoConnectorResponseV1(ConnectorResponseV1, KlaviyoConfigV1)
```



## KustomerConnectorResponseV1 Objects

```python
class KustomerConnectorResponseV1(ConnectorResponseV1, KustomerConfigV1)
```



## LeverConnectorResponseV1 Objects

```python
class LeverConnectorResponseV1(ConnectorResponseV1, LeverConfigV1)
```



## LightSpeedRetailConnectorResponseV1 Objects

```python
class LightSpeedRetailConnectorResponseV1(ConnectorResponseV1,
                                          LightSpeedRetailConfigV1)
```



## LinkedinAdsConnectorResponseV1 Objects

```python
class LinkedinAdsConnectorResponseV1(ConnectorResponseV1, LinkedinAdsConfigV1)
```



## LinkedinCompanyPagesConnectorResponseV1 Objects

```python
class LinkedinCompanyPagesConnectorResponseV1(ConnectorResponseV1,
                                              LinkedinCompanyPagesConfigV1)
```



## MagentoMysqlConnectorResponseV1 Objects

```python
class MagentoMysqlConnectorResponseV1(ConnectorResponseV1,
                                      MagentoMysqlConfigV1)
```



## MagentoMysqlRdsConnectorResponseV1 Objects

```python
class MagentoMysqlRdsConnectorResponseV1(ConnectorResponseV1,
                                         MagentoMysqlRdsConfigV1)
```



## MailchimpConnectorResponseV1 Objects

```python
class MailchimpConnectorResponseV1(ConnectorResponseV1, MailchimpConfigV1)
```



## MandrillConnectorResponseV1 Objects

```python
class MandrillConnectorResponseV1(ConnectorResponseV1, MandrillConfigV1)
```



## MariaConnectorResponseV1 Objects

```python
class MariaConnectorResponseV1(ConnectorResponseV1, MariaConfigV1)
```



## MariaAzureConnectorResponseV1 Objects

```python
class MariaAzureConnectorResponseV1(ConnectorResponseV1, MariaAzureConfigV1)
```



## MariaRdsConnectorResponseV1 Objects

```python
class MariaRdsConnectorResponseV1(ConnectorResponseV1, MariaRdsConfigV1)
```



## MarinConnectorResponseV1 Objects

```python
class MarinConnectorResponseV1(ConnectorResponseV1, MarinConfigV1)
```



## MarketoConnectorResponseV1 Objects

```python
class MarketoConnectorResponseV1(ConnectorResponseV1, MarketoConfigV1)
```



## MavenlinkConnectorResponseV1 Objects

```python
class MavenlinkConnectorResponseV1(ConnectorResponseV1, MavenlinkConfigV1)
```



## MedalliaConnectorResponseV1 Objects

```python
class MedalliaConnectorResponseV1(ConnectorResponseV1, MedalliaConfigV1)
```



## MicrosoftListsConnectorResponseV1 Objects

```python
class MicrosoftListsConnectorResponseV1(ConnectorResponseV1,
                                        MicrosoftListsConfigV1)
```



## MixpanelConnectorResponseV1 Objects

```python
class MixpanelConnectorResponseV1(ConnectorResponseV1, MixpanelConfigV1)
```



## MongoConnectorResponseV1 Objects

```python
class MongoConnectorResponseV1(ConnectorResponseV1, MongoConfigV1)
```



## MongoShardedConnectorResponseV1 Objects

```python
class MongoShardedConnectorResponseV1(ConnectorResponseV1,
                                      MongoShardedConfigV1)
```



## MysqlConnectorResponseV1 Objects

```python
class MysqlConnectorResponseV1(ConnectorResponseV1, MysqlConfigV1)
```



## MysqlAzureConnectorResponseV1 Objects

```python
class MysqlAzureConnectorResponseV1(ConnectorResponseV1, MysqlAzureConfigV1)
```



## MysqlRdsConnectorResponseV1 Objects

```python
class MysqlRdsConnectorResponseV1(ConnectorResponseV1, MysqlRdsConfigV1)
```



## NetsuiteSuiteanalyticsConnectorResponseV1 Objects

```python
class NetsuiteSuiteanalyticsConnectorResponseV1(ConnectorResponseV1,
                                                NetsuiteSuiteanalyticsConfigV1
                                                )
```



## OneDriveConnectorResponseV1 Objects

```python
class OneDriveConnectorResponseV1(ConnectorResponseV1, OneDriveConfigV1)
```



## OptimizelyConnectorResponseV1 Objects

```python
class OptimizelyConnectorResponseV1(ConnectorResponseV1, OptimizelyConfigV1)
```



## OracleConnectorResponseV1 Objects

```python
class OracleConnectorResponseV1(ConnectorResponseV1, OracleConfigV1)
```



## OracleEbsConnectorResponseV1 Objects

```python
class OracleEbsConnectorResponseV1(ConnectorResponseV1, OracleEbsConfigV1)
```



## OracleHvaConnectorResponseV1 Objects

```python
class OracleHvaConnectorResponseV1(ConnectorResponseV1, OracleHvaConfigV1)
```



## OracleRacConnectorResponseV1 Objects

```python
class OracleRacConnectorResponseV1(ConnectorResponseV1, OracleRacConfigV1)
```



## OracleRdsConnectorResponseV1 Objects

```python
class OracleRdsConnectorResponseV1(ConnectorResponseV1, OracleRdsConfigV1)
```



## OutbrainConnectorResponseV1 Objects

```python
class OutbrainConnectorResponseV1(ConnectorResponseV1, OutbrainConfigV1)
```



## OutreachConnectorResponseV1 Objects

```python
class OutreachConnectorResponseV1(ConnectorResponseV1, OutreachConfigV1)
```



## PardotConnectorResponseV1 Objects

```python
class PardotConnectorResponseV1(ConnectorResponseV1, PardotConfigV1)
```



## PaypalConnectorResponseV1 Objects

```python
class PaypalConnectorResponseV1(ConnectorResponseV1, PaypalConfigV1)
```



## PaypalSandboxConnectorResponseV1 Objects

```python
class PaypalSandboxConnectorResponseV1(ConnectorResponseV1,
                                       PaypalSandboxConfigV1)
```



## PendoConnectorResponseV1 Objects

```python
class PendoConnectorResponseV1(ConnectorResponseV1, PendoConfigV1)
```



## PinterestAdsConnectorResponseV1 Objects

```python
class PinterestAdsConnectorResponseV1(ConnectorResponseV1,
                                      PinterestAdsConfigV1)
```



## PipedriveConnectorResponseV1 Objects

```python
class PipedriveConnectorResponseV1(ConnectorResponseV1, PipedriveConfigV1)
```



## PostgresConnectorResponseV1 Objects

```python
class PostgresConnectorResponseV1(ConnectorResponseV1, PostgresConfigV1)
```



## PostgresRdsConnectorResponseV1 Objects

```python
class PostgresRdsConnectorResponseV1(ConnectorResponseV1, PostgresRdsConfigV1)
```



## QualtricsConnectorResponseV1 Objects

```python
class QualtricsConnectorResponseV1(ConnectorResponseV1, QualtricsConfigV1)
```



## QuickbooksConnectorResponseV1 Objects

```python
class QuickbooksConnectorResponseV1(ConnectorResponseV1, QuickbooksConfigV1)
```



## RechargeConnectorResponseV1 Objects

```python
class RechargeConnectorResponseV1(ConnectorResponseV1, RechargeConfigV1)
```



## RecurlyConnectorResponseV1 Objects

```python
class RecurlyConnectorResponseV1(ConnectorResponseV1, RecurlyConfigV1)
```



## RedditAdsConnectorResponseV1 Objects

```python
class RedditAdsConnectorResponseV1(ConnectorResponseV1, RedditAdsConfigV1)
```



## S3ConnectorResponseV1 Objects

```python
class S3ConnectorResponseV1(ConnectorResponseV1, S3ConfigV1)
```



## SageIntacctConnectorResponseV1 Objects

```python
class SageIntacctConnectorResponseV1(ConnectorResponseV1, SageIntacctConfigV1)
```



## SailthruConnectorResponseV1 Objects

```python
class SailthruConnectorResponseV1(ConnectorResponseV1, SailthruConfigV1)
```



## SalesforceConnectorResponseV1 Objects

```python
class SalesforceConnectorResponseV1(ConnectorResponseV1, SalesforceConfigV1)
```



## SalesforceMarketingCloudConnectorResponseV1 Objects

```python
class SalesforceMarketingCloudConnectorResponseV1(
        ConnectorResponseV1, SalesforceMarketingCloudConfigV1)
```



## SalesforceSandboxConnectorResponseV1 Objects

```python
class SalesforceSandboxConnectorResponseV1(ConnectorResponseV1,
                                           SalesforceSandboxConfigV1)
```



## SapBusinessByDesignConnectorResponseV1 Objects

```python
class SapBusinessByDesignConnectorResponseV1(ConnectorResponseV1,
                                             SapBusinessByDesignConfigV1)
```



## SegmentConnectorResponseV1 Objects

```python
class SegmentConnectorResponseV1(ConnectorResponseV1, SegmentConfigV1)
```



## SendgridConnectorResponseV1 Objects

```python
class SendgridConnectorResponseV1(ConnectorResponseV1, SendgridConfigV1)
```



## ServicenowConnectorResponseV1 Objects

```python
class ServicenowConnectorResponseV1(ConnectorResponseV1, ServicenowConfigV1)
```



## SftpConnectorResponseV1 Objects

```python
class SftpConnectorResponseV1(ConnectorResponseV1, SftpConfigV1)
```



## SharePointConnectorResponseV1 Objects

```python
class SharePointConnectorResponseV1(ConnectorResponseV1, SharePointConfigV1)
```



## ShopifyConnectorResponseV1 Objects

```python
class ShopifyConnectorResponseV1(ConnectorResponseV1, ShopifyConfigV1)
```



## SnapchatAdsConnectorResponseV1 Objects

```python
class SnapchatAdsConnectorResponseV1(ConnectorResponseV1, SnapchatAdsConfigV1)
```



## SnowplowConnectorResponseV1 Objects

```python
class SnowplowConnectorResponseV1(ConnectorResponseV1, SnowplowConfigV1)
```



## SplunkConnectorResponseV1 Objects

```python
class SplunkConnectorResponseV1(ConnectorResponseV1, SplunkConfigV1)
```



## SqlServerConnectorResponseV1 Objects

```python
class SqlServerConnectorResponseV1(ConnectorResponseV1, SqlServerConfigV1)
```



## SqlServerHvaConnectorResponseV1 Objects

```python
class SqlServerHvaConnectorResponseV1(ConnectorResponseV1,
                                      SqlServerHvaConfigV1)
```



## SqlServerRdsConnectorResponseV1 Objects

```python
class SqlServerRdsConnectorResponseV1(ConnectorResponseV1,
                                      SqlServerRdsConfigV1)
```



## SquareConnectorResponseV1 Objects

```python
class SquareConnectorResponseV1(ConnectorResponseV1, SquareConfigV1)
```



## StripeConnectorResponseV1 Objects

```python
class StripeConnectorResponseV1(ConnectorResponseV1, StripeConfigV1)
```



## StripeTestConnectorResponseV1 Objects

```python
class StripeTestConnectorResponseV1(ConnectorResponseV1, StripeTestConfigV1)
```



## SurveyMonkeyConnectorResponseV1 Objects

```python
class SurveyMonkeyConnectorResponseV1(ConnectorResponseV1,
                                      SurveyMonkeyConfigV1)
```



## TaboolaConnectorResponseV1 Objects

```python
class TaboolaConnectorResponseV1(ConnectorResponseV1, TaboolaConfigV1)
```



## TiktokAdsConnectorResponseV1 Objects

```python
class TiktokAdsConnectorResponseV1(ConnectorResponseV1, TiktokAdsConfigV1)
```



## TwilioConnectorResponseV1 Objects

```python
class TwilioConnectorResponseV1(ConnectorResponseV1, TwilioConfigV1)
```



## TwitterConnectorResponseV1 Objects

```python
class TwitterConnectorResponseV1(ConnectorResponseV1, TwitterConfigV1)
```



## TwitterAdsConnectorResponseV1 Objects

```python
class TwitterAdsConnectorResponseV1(ConnectorResponseV1, TwitterAdsConfigV1)
```



## TypeformConnectorResponseV1 Objects

```python
class TypeformConnectorResponseV1(ConnectorResponseV1, TypeformConfigV1)
```



## UservoiceConnectorResponseV1 Objects

```python
class UservoiceConnectorResponseV1(ConnectorResponseV1, UservoiceConfigV1)
```



## WebhooksConnectorResponseV1 Objects

```python
class WebhooksConnectorResponseV1(ConnectorResponseV1, WebhooksConfigV1)
```



## WoocommerceConnectorResponseV1 Objects

```python
class WoocommerceConnectorResponseV1(ConnectorResponseV1, WoocommerceConfigV1)
```



## WorkdayConnectorResponseV1 Objects

```python
class WorkdayConnectorResponseV1(ConnectorResponseV1, WorkdayConfigV1)
```



## WorkdayHcmConnectorResponseV1 Objects

```python
class WorkdayHcmConnectorResponseV1(ConnectorResponseV1, WorkdayHcmConfigV1)
```



## XeroConnectorResponseV1 Objects

```python
class XeroConnectorResponseV1(ConnectorResponseV1, XeroConfigV1)
```



## YahooGeminiConnectorResponseV1 Objects

```python
class YahooGeminiConnectorResponseV1(ConnectorResponseV1, YahooGeminiConfigV1)
```



## YoutubeAnalyticsConnectorResponseV1 Objects

```python
class YoutubeAnalyticsConnectorResponseV1(ConnectorResponseV1,
                                          YoutubeAnalyticsConfigV1)
```



## ZendeskConnectorResponseV1 Objects

```python
class ZendeskConnectorResponseV1(ConnectorResponseV1, ZendeskConfigV1)
```



## ZendeskChatConnectorResponseV1 Objects

```python
class ZendeskChatConnectorResponseV1(ConnectorResponseV1, ZendeskChatConfigV1)
```



## ZendeskSellConnectorResponseV1 Objects

```python
class ZendeskSellConnectorResponseV1(ConnectorResponseV1, ZendeskSellConfigV1)
```



## ZendeskSunshineConnectorResponseV1 Objects

```python
class ZendeskSunshineConnectorResponseV1(ConnectorResponseV1,
                                         ZendeskSunshineConfigV1)
```



## ZohoCrmConnectorResponseV1 Objects

```python
class ZohoCrmConnectorResponseV1(ConnectorResponseV1, ZohoCrmConfigV1)
```



## ZuoraConnectorResponseV1 Objects

```python
class ZuoraConnectorResponseV1(ConnectorResponseV1, ZuoraConfigV1)
```



## ZuoraSandboxConnectorResponseV1 Objects

```python
class ZuoraSandboxConnectorResponseV1(ConnectorResponseV1,
                                      ZuoraSandboxConfigV1)
```



## V1ConnectorsConnectorIdTestPostResponse Objects

```python
class V1ConnectorsConnectorIdTestPostResponse(BaseModel)
```



## V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse Objects

```python
class V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse(
        BaseModel)
```



## V1ConnectorsConnectorIdGetResponse Objects

```python
class V1ConnectorsConnectorIdGetResponse(BaseModel)
```



## V1ConnectorsConnectorIdPatchResponse Objects

```python
class V1ConnectorsConnectorIdPatchResponse(BaseModel)
```



## V1ConnectorsPostResponse Objects

```python
class V1ConnectorsPostResponse(BaseModel)
```



## SchemaConfigResponse Objects

```python
class SchemaConfigResponse(BaseModel)
```



## StandardConfigResponse Objects

```python
class StandardConfigResponse(BaseModel)
```



## V1ConnectorsConnectorIdSchemasSchemaNameTablesTableNameColumnsColumnNamePatchResponse Objects

```python
class V1ConnectorsConnectorIdSchemasSchemaNameTablesTableNameColumnsColumnNamePatchResponse(
        BaseModel)
```



## V1ConnectorsConnectorIdSchemasGetResponse Objects

```python
class V1ConnectorsConnectorIdSchemasGetResponse(BaseModel)
```



## V1ConnectorsConnectorIdSchemasPatchResponse Objects

```python
class V1ConnectorsConnectorIdSchemasPatchResponse(BaseModel)
```



## V1ConnectorsConnectorIdSchemasSchemaNamePatchResponse Objects

```python
class V1ConnectorsConnectorIdSchemasSchemaNamePatchResponse(BaseModel)
```



## V1ConnectorsConnectorIdSchemasReloadPostResponse Objects

```python
class V1ConnectorsConnectorIdSchemasReloadPostResponse(BaseModel)
```



## V1ConnectorsConnectorIdSchemasSchemaNameTablesTableNamePatchResponse Objects

```python
class V1ConnectorsConnectorIdSchemasSchemaNameTablesTableNamePatchResponse(
        BaseModel)
```
