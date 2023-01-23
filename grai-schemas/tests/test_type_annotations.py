from grai_schemas.models import ColumnMetadata, NodeTypes, TableMetadata


class TestColumnObjTyping:
    obj_fields = ColumnMetadata.__fields__

    def test_node_type_values(self):
        # Type annotation is validated by static type checker
        model_field = self.obj_fields["node_type"]
        assert (
            model_field.default == NodeTypes.column.value
        ), "Default value for {node_type} must be the same as defined on the NodeTypes object"


class TestTableObjTyping:
    obj_fields = TableMetadata.__fields__

    def test_node_type_values(self):
        # Type annotation is validated by static type checker
        model_field = self.obj_fields["node_type"]
        assert (
            model_field.default == NodeTypes.table.value
        ), "Default value for {node_type} must be the same as defined on the NodeTypes object"
