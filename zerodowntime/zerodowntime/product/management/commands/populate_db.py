import warnings
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from faker import Factory

from ...models import Product

fake = Factory.create()


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--amount",
            default=1000000,
            help=(
                "Populate db with example products. The default value is 1 000 000, "
                "the max value is 5 000 000."
            ),
            type=int,
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        amount = options["amount"]
        if amount > 5000000:
            warnings.warn(
                "The max value of amount is 5 000 000, "
                "the amount has been changed to that value."
            )
            amount = 1000000
        start_pk = Product.objects.last().pk
        Product.objects.bulk_create(
            [
                Product(
                    name=f"Test-product-{start_pk + i + 1}", description=fake.text()
                )
                for i in range(amount)
            ],
            batch_size=100000,
        )
