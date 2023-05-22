from django.apps import apps as registry
from django.db import migrations
from django.db.models.signals import post_migrate

from .tasks.v0_01 import create_slugs_for_products_task


def create_unique_slugs_for_products(apps, schema_editor):
    def on_migrations_complete(sender=None, **kwargs):
        create_slugs_for_products_task.delay()

    sender = registry.get_app_config("product")
    post_migrate.connect(on_migrations_complete, weak=False, sender=sender)


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0002_product_slug"),
    ]

    operations = [
        migrations.RunPython(
            create_unique_slugs_for_products, migrations.RunPython.noop
        ),
    ]
