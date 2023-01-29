import uuid

from django.db.models import fields

from rest_framework import serializers

from .models import Edge, Node


class NodeSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(required=False)

    class Meta:
        model = Node
        fields = (
            "id",
            "namespace",
            "name",
            "display_name",
            "data_source",
            "metadata",
            "is_active",
        )
        read_only_fields = ("created_at", "updated_at")


# from django.forms.models import model_to_dict
# class EdgeNodeSerializer(serializers.RelatedField):
#     name = serializers.CharField(required=False)
#     namespace = serializers.CharField(required=False)
#     id = serializers.CharField(required=False)
#
#     queryset = Node.objects.all()
#
#     def to_internal_value(self, instance):
#         match instance:
#             case str() as node_id:
#                 # raise Exception(self.request.data['source'], node_id)
#                 result = self.queryset.filter(id=node_id).first()
#             case uuid.UUID() as node_id:
#                 result = self.queryset.filter(id=node_id).first()
#             case {'id': node_id} if node_id:
#                 result = self.queryset.filter(id=node_id).first()
#             case {'name': name, 'namespace': namespace} if name and namespace:
#                 result = self.queryset.filter(name=name, namespace=namespace).first()
#             case _:
#                 raise Exception(f'fail {instance}, {type(instance)}')
#         #raise Exception(f"{instance} || {result}")
#         return result
#
#     def to_representation(self, instance):
#         return model_to_dict(instance)
#
#     class Meta:
#         depth = 1

# class EdgeNodeSerializer(serializers.RelatedField):
#     id = serializers.UUIDField(default=uuid.uuid4, required=False)
#     namespace = serializers.CharField(max_length=255, default="default")
#     name = serializers.CharField(max_length=255)


class EdgeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    display_name = serializers.CharField(required=False)

    class Meta:
        model = Edge
        fields = (
            "id",
            "name",
            "display_name",
            "namespace",
            "data_source",
            "metadata",
            "is_active",
            "source",
            "destination",
        )
        read_only_fields = ("created_at", "updated_at")
