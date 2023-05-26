from django.db import migrations
from django.utils.text import slugify

# Results in memory usage of ~20MB, each update takes ~ 1s
BATCH_SIZE = 500


def create_unique_slugs_for_products(apps, schema_editor):
    Product = apps.get_model("product", "Product")
    create_slugs_for_products_task(Product)


def create_slugs_for_products_task(product_model):
    products = product_model.objects.filter(slug__isnull=True).order_by("name")
    product = products.first()
    if not product:
        return
    first_char = product.name[0].lower()
    products = products.filter(name__istartswith=first_char).order_by("name")
    if products.exists():
        slugs = list(
            product_model.objects.filter(slug__istartswith=first_char).values_list(
                "slug", flat=True
            )
        )
        if products.count() > BATCH_SIZE:
            ids = products.values_list("id", flat=True)[:BATCH_SIZE]
            products = product_model.objects.filter(pk__in=ids)
        create_slugs_for_products(product_model, products, slugs)
        create_slugs_for_products_task(product_model)


def create_slugs_for_products(product_model, products, slugs):
    """Create unique slug for Product instances."""
    products_to_update = []
    for product in products:
        slug = generate_unique_slug(product, slugs)
        slugs.append(slug)
        product.slug = slug
        products_to_update.append(product)
    product_model.objects.bulk_update(products_to_update, ["slug"])


def generate_unique_slug(instance, slug_values):
    slug = slugify(instance.name)
    unique_slug = slug
    extension = 1

    while unique_slug in slug_values:
        extension += 1
        unique_slug = f"{slug}-{extension}"

    return unique_slug


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0002_product_slug"),
    ]

    operations = [
        migrations.RunPython(
            create_unique_slugs_for_products, migrations.RunPython.noop
        ),
    ]
