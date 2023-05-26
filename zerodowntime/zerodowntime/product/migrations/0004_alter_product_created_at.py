from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0003_populate_created_at"),
    ]

    operations = [
        # set the default value for new instances
        # the new instances will get the current date time
        migrations.AlterField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
