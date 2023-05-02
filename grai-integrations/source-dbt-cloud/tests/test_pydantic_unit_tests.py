# import pydantic
#
# from grai_source_dbt.models.tests import Test
#
#
# def test_build_DBTTest():
#     test_obj = {
#         "raw_sql": "{{ test_unique(**_dbt_generic_test_kwargs) }}",
#         "test_metadata": {
#             "name": "unique",
#             "kwargs": {
#                 "column_name": "customer_id",
#                 "model": "{{ get_where_subquery(ref('customers')) }}",
#             },
#             "namespace": None,
#         },
#         "resource_type": "test",
#         "depends_on": {
#             "macros": ["macro.dbt.test_unique"],
#             "nodes": ["model.jaffle_shop.customers"],
#         },
#         "config": {
#             "enabled": True,
#             "alias": None,
#             "schema": "dbt_test__audit",
#             "database": None,
#             "tags": [],
#             "meta": {},
#             "materialized": "test",
#             "severity": "ERROR",
#             "store_failures": None,
#             "where": None,
#             "limit": None,
#             "fail_calc": "count(*)",
#             "warn_if": "!= 0",
#             "error_if": "!= 0",
#         },
#         "database": "docker",
#         "schema": "dbt_alice_dbt_test__audit",
#         "fqn": ["jaffle_shop", "unique_customers_customer_id"],
#         "unique_id": "test.jaffle_shop.unique_customers_customer_id.c5af1ff4b1",
#         "package_name": "jaffle_shop",
#         "root_path": "/Users/ian/repos/grai/jaffle_shop",
#         "path": "unique_customers_customer_id.sql",
#         "original_file_path": "models/schema.yml",
#         "name": "unique_customers_customer_id",
#         "alias": "unique_customers_customer_id",
#         "checksum": {"name": "none", "checksum": ""},
#         "tags": [],
#         "refs": [["customers"]],
#         "sources": [],
#         "description": "",
#         "columns": {},
#         "meta": {},
#         "docs": {"show": True},
#         "patch_path": None,
#         "compiled_path": None,
#         "build_path": None,
#         "deferred": False,
#         "unrendered_config": {},
#         "created_at": 1667500551.437151,
#         "column_name": "customer_id",
#         "file_key_name": "models.customers",
#     }
#
#     result = Test(**test_obj)
