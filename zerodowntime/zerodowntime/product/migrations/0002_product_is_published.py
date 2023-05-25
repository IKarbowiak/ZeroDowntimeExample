from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        # add the new column `is_published` in the DB
        # set the `true` value on all existing instances
        migrations.AddField(
            model_name="product",
            name="is_published",
            field=models.BooleanField(default=True),
        ),
        # set the default value for new instances
        migrations.RunSQL(
            """
                ALTER TABLE product_product
                ALTER COLUMN is_published
                SET DEFAULT true;
            """
        ),
    ]
