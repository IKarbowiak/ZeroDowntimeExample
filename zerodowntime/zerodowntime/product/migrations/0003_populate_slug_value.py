from django.db import migrations
from django.db.models import F
from django.utils.text import slugify

BATCH_SIZE = 1000


def create_unique_slugs_for_products(apps, schema_editor):
    Product = apps.get_model("product", "Product")
    create_slugs_for_products_task(Product)


def create_slugs_for_products_task(product_model):
    # TODO: consider rewriting it to create the unique slug
    products = product_model.objects.filter(slug__isnull=True).order_by("pk")
    ids = products.values_list("pk", flat=True)[:BATCH_SIZE]
    if ids:
        product_qs = product_model.objects.filter(pk__in=ids)
        create_slugs_for_products(product_qs)
        create_slugs_for_products_task()


def create_slugs_for_products(products):
    """Create slug for Product instances."""
    products.update(slug=slugify(F("name")))


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0002_product_slug"),
    ]

    operations = [
        migrations.RunPython(
            create_unique_slugs_for_products, migrations.RunPython.noop
        ),
    ]
