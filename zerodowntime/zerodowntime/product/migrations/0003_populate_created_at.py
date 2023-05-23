from django.db import migrations
from django.db.models import F

BATCH_SIZE = 1000


def set_created_at_value(apps, _schema_editor):
    Product = apps.get_model("product", "Product")
    set_product_created_at_value_task(Product)


def set_product_created_at_value_task(product_model):
    events = product_model.objects.filter(created_at__isnull=True).order_by("pk")
    ids = events.values_list("pk", flat=True)[:BATCH_SIZE]
    products_qs = product_model.objects.filter(pk__in=ids)
    if ids:
        set_product_created_at_value(products_qs)
        set_product_created_at_value_task()


def set_product_created_at_value(products_qs):
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
