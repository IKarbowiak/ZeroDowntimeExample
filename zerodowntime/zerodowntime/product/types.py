import graphene
from graphene.types.objecttype import ObjectType


class Product(ObjectType):
    name = graphene.String(description="The name of the product.")
    description = graphene.String(description="Description of the product.")
    created = graphene.DateTime(
        description="The date time when the product was created"
    )

    class Meta:
        interfaces = [graphene.relay.Node]
