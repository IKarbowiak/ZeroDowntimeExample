from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_published",
            field=models.BooleanField(default=True),
        ),
        migrations.RunSQL(
            """
                ALTER TABLE product_product
                ALTER COLUMN is_published
                SET DEFAULT true;
            """
        ),
    ]
