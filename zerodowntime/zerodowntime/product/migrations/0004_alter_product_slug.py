from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0003_populate_slug_value"),
    ]

    operations = [
        # change the field into non-nullable
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
