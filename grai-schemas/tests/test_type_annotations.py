from grai_schemas.v1.metadata.nodes import ColumnMetadata, NodeTypeLabels, TableMetadata

# Goal is to test that each node type in the Enum is covered by a corresponding model literal

# class TestColumnObjTyping:
#     obj_fields = ColumnMetadata.__fields__
#
#     def test_node_type_values(self):
#         # Type annotation is validated by static type checker
#         model_field = self.obj_fields["node_type"]
#         assert (
#             model_field.default == NodeTypes.column.value
#         ), f"Default value for {model_field} must be the same as defined on the NodeTypes object"
#
#
# class TestTableObjTyping:
#     obj_fields = TableMetadata.__fields__
#
#     def test_node_type_values(self):
#         # Type annotation is validated by static type checker
#         model_field = self.obj_fields["node_type"]
#         assert (
#             model_field.default == NodeTypes.table.value
#         ), f"Default value for {model_field} must be the same as defined on the NodeTypes object"
