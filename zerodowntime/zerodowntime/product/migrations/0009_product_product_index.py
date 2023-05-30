from django.contrib.postgres.operations import AddIndexConcurrently
from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("product", "0008_merge_20230527_0946"),
    ]

    operations = [
        AddIndexConcurrently(
            model_name="product",
            index=models.Index(fields=["name", "slug"], name="product_index"),
        )
    ]
