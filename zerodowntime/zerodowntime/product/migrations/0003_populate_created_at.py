from django.db import migrations, transaction
from django.db.models import F

# Results in memory usage of ~20MB, each update takes < 1s
BATCH_SIZE = 5000


def set_created_at_value(apps, _schema_editor):
    Product = apps.get_model("product", "Product")
    set_product_created_at_value_task(Product)


def set_product_created_at_value_task(product_model):
    # take the products that has empty `created_at` value, order them by `pk`
    products = product_model.objects.filter(created_at__isnull=True).order_by("pk")

    # take the ids of the first 5000 objects
    ids = products.values_list("pk", flat=True)[:BATCH_SIZE]

    # get the first 5000 objects, run one more db query to avoid using insufficient
    # limit and offset SQL statement
    products_qs = product_model.objects.filter(pk__in=ids)
    if ids:
        # call the method for update the instances
        set_product_created_at_value(products_qs)

        # run the function again to update the rest of instances
        set_product_created_at_value_task(product_model)


def set_product_created_at_value(products_qs):
    with transaction.atomic():
        _products = list(products_qs.select_for_update(of=(["self"])))
        products_qs.update(created_at=F("created"))


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0002_product_created_at"),
    ]

    operations = [
        migrations.RunPython(
            set_created_at_value, reverse_code=migrations.RunPython.noop
        ),
    ]
