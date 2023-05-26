from django.db import transaction
from django.db.models import F
from django.utils.text import slugify

from ....celeryconf import app
from ...models import Product


@app.task
def create_slugs_for_products_task():
    # Results in memory usage of ~20MB, each update takes ~ 1s
    BATCH_SIZE = 1000

    products = Product.objects.filter(slug__isnull=True).order_by("name")
    product = products.first()
    if not product:
        return
    first_char = product.name[0].lower()
    products = products.filter(name__istartswith=first_char).order_by("name")
    if products.exists():
        slugs = list(
            Product.objects.filter(slug__istartswith=first_char).values_list(
                "slug", flat=True
            )
        )
        if products.count() > BATCH_SIZE:
            ids = products.values_list("id", flat=True)[:BATCH_SIZE]
            products = Product.objects.filter(pk__in=ids)
        create_slugs_for_products(products, slugs)
        create_slugs_for_products_task.delay()


def create_slugs_for_products(products, slugs):
    """Create unique slug for Product instances."""
    products_to_update = []
    for product in products:
        slug = generate_unique_slug(product, slugs)
        slugs.append(slug)
        product.slug = slug
        products_to_update.append(product)
    Product.objects.bulk_update(products_to_update, ["slug"])


def generate_unique_slug(instance, slug_values):
    slug = slugify(instance.name)
    unique_slug = slug
    extension = 1

    while unique_slug in slug_values:
        extension += 1
        unique_slug = f"{slug}-{extension}"

    return unique_slug


@app.task
def set_product_created_at_value_task():
    # Results in memory usage of ~20MB, each update takes < 1s
    BATCH_SIZE = 5000

    # take the products that has empty `created_at` value, order them by `pk`
    products = Product.objects.filter(created_at__isnull=True).order_by("pk")

    # take the ids of the first 5000 objects
    ids = products.values_list("pk", flat=True)[:BATCH_SIZE]

    # get the first 5000 objects, run one more db query to avoid using insufficient
    # limit and offset SQL statement
    products_qs = Product.objects.filter(pk__in=ids)
    if ids:
        # call the method for update the instances
        set_product_created_at_value(products_qs)

        # run the task again to update the rest of instances
        set_product_created_at_value_task.delay()


def set_product_created_at_value(products_qs):
    with transaction.atomic():
        # lock the batch of objects to avoid the deadlock
        _products = list(products_qs.select_for_update(of=(["self"])))
        products_qs.update(created_at=F("created"))
