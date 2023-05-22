from django.db import transaction
from django.db.models import F
from django.utils.text import slugify

from ....celeryconf import app
from ...models import Product

# TODO: calulate this value
BATCH_SIZE = 1000


@app.task
def create_slugs_for_products_task():
    # TODO: consider rewriting it to create the unique slug
    products = Product.objects.filter(slug__isnull=True).order_by("pk")
    ids = products.values_list("pk", flat=True)[:BATCH_SIZE]
    if ids:
        product_qs = Product.objects.filter(pk__in=ids)
        create_slugs_for_products(product_qs)
        create_slugs_for_products_task.delay()


def create_slugs_for_products(products):
    """Create slug for Product instances."""
    with transaction.atomic():
        _products = list(products.select_for_update(of=(["self"])))
        products.update(slug=slugify(F("name")))
