from django.apps import apps as registry
from django.db import migrations
from django.db.models.signals import post_migrate

from .tasks.v0_01 import set_product_created_at_value_task


def set_created_at_value(apps, _schema_editor):
    def on_migrations_complete(sender=None, **kwargs):
        set_product_created_at_value_task.delay()

    sender = registry.get_app_config("product")
    post_migrate.connect(on_migrations_complete, weak=False, sender=sender)


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0002_product_created_at"),
    ]

    operations = [
        migrations.RunPython(
            set_created_at_value, reverse_code=migrations.RunPython.noop
        ),
    ]
