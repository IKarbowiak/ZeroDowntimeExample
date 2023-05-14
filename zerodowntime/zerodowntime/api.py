import binascii

import graphene
from graphql.error import GraphQLError

from .product import models
from .product.mutations import ProductCreate, ProductDelete
from .product.types import Product


class Query(graphene.ObjectType):
    product = graphene.Field(
        Product, id=graphene.Argument(graphene.ID, description="ID of the product")
    )

    def resolve_product(root, info, id):
        try:
            type_, id = graphene.Node.resolve_global_id(info, id)
        except (binascii.Error, UnicodeDecodeError, ValueError):
            raise GraphQLError(f"Couldn't resolve id: {id}.")
        return models.Product.objects.filter(pk=id).first()


class Mutation(graphene.ObjectType):
    product_create = ProductCreate.Field()
    product_delete = ProductDelete.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
