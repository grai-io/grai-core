from grai_schemas.models import Column, NodeTypes, Table


class TestColumnObjTyping:
    obj_fields = Column.__fields__

    def test_node_type_values(self):
        # Type annotation is validated by static type checker
        model_field = self.obj_fields["node_type"]
        assert (
            model_field.default == NodeTypes.column.value
        ), "Default value for {node_type} must be the same as defined on the NodeTypes object"


class TestTableObjTyping:
    obj_fields = Table.__fields__

    def test_node_type_values(self):
        # Type annotation is validated by static type checker
        model_field = self.obj_fields["node_type"]
        assert (
            model_field.default == NodeTypes.table.value
        ), "Default value for {node_type} must be the same as defined on the NodeTypes object"
