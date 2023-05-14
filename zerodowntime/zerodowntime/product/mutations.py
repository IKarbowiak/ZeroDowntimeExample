import binascii

import graphene
from django.core.exceptions import ValidationError

from . import models
from .types import Product


class ProductCreate(graphene.Mutation):
    product = graphene.Field(Product, description="Created product.")

    class Arguments:
        name = graphene.String(description="The name of the product")
        description = graphene.JSONString(description="The description of the product.")

    class Meta:
        description = "Create a product"

    @classmethod
    def mutate(cls, root, info, name, description):
        if not name.strip():
            raise ValidationError("You need to provide a value for the `name` field.")
        product = models.Product.objects.create(name=name, description=description)
        return cls(product)


class ProductDelete(graphene.Mutation):
    product = graphene.Field(Product, description="Deleted product.")

    class Arguments:
        id = graphene.ID(description="The ID of the product to delete.")

    class Meta:
        description = "Delete a product"

    @classmethod
    def mutate(cls, root, info, id):
        error_msg = f"Couldn't resolve id: {id}."
        try:
            type_, pk = graphene.Node.resolve_global_id(info, id)
        except (binascii.Error, UnicodeDecodeError, ValueError):
            raise ValidationError(error_msg)

        product = models.Product.objects.filter(id=pk)
        if not product:
            raise ValidationError(error_msg)

        product.delete()

        product.id = pk

        return cls(product=product)
