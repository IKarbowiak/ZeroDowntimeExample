from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0006_remove_product_created_alter_product_created_at"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                # remove the `created` column from the DB
                migrations.RunSQL(
                    sql="""
                        ALTER TABLE product_product
                        DROP COLUMN created;
                    """,
                )
            ],
        )
    ]
