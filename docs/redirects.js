module.exports = [
    {
        source: "/web-app/connections",
        destination: "/integrations/support-status",
        permanent: true,
    },
    {
        source: "/integrations/looker",
        destination: "/integrations/business_intelligence/looker",
        permanent: true,
    },
    {
        source: "/integrations/metabase",
        destination: "/integrations/business_intelligence/metabase",
        permanent: true,
    },
    {
        source: "/integrations/bigquery",
        destination: "/integrations/data_warehouses/bigquery",
        permanent: true,
    },
    {
        source: "/integrations/redshift",
        destination: "/integrations/data_warehouses/redshift",
        permanent: true,
    },
    {
        source: "/integrations/snowflake",
        destination: "/integrations/data_warehouses/snowflake",
        permanent: true,
    },
    {
        source: "/integrations/mssql",
        destination: "/integrations/databases/mssql",
        permanent: true,
    },
    {
        source: "/integrations/mysql",
        destination: "/integrations/databases/mysql",
        permanent: true,
    },
    {
        source: "/integrations/postgres",
        destination: "/integrations/databases/postgres",
        permanent: true,
    },
    {
        source: "/integrations/dbt-cloud",
        destination: "/integrations/etl/dbt-cloud",
        permanent: true,
    },
    {
        source: "/integrations/dbt",
        destination: "/integrations/etl/dbt",
        permanent: true,
    },
    {
        source: "/integrations/fivetran",
        destination: "/integrations/etl/fivetran",
        permanent: true,
    },
    {
        source: "/integrations/flat-file",
        destination: "/integrations/misc/flat-file",
        permanent: true,
    },
    {
        source: "/integrations/openlineage",
        destination: "/integrations/misc/openlineage",
        permanent: true,
    },
    {
        source: "/integrations/yaml",
        destination: "/integrations/misc/yaml",
        permanent: true,
    },
    {
        source: "/integrations/airflow",
        destination: "/integrations/orchestration/airflow",
        permanent: true,
    },
    {
        source: "/connectors/:slug",
        destination: "/integrations/:slug",
        permanent: true,
    },
];
