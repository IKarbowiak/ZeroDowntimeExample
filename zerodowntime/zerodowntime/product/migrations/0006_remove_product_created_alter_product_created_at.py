from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0004_alter_product_created_at"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            # set the `created` column in DB as a nullable
            database_operations=[
                migrations.AlterField(
                    model_name="product",
                    name="created",
                    field=models.DateTimeField(blank=True, null=True),
                ),
            ],
            # remove the `created` field from the ORM
            state_operations=[
                migrations.RemoveField(
                    model_name="product",
                    name="created",
                ),
            ],
        ),
        migrations.AlterField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
