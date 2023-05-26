from django.utils.text import slugify

from .models import Product


def generate_unique_slug(name):
    slug = slugify(name)
    slug_values = list(
        Product.objects.filter(slug__istartswith=slug).values_list("slug", flat=True)
    )
    unique_slug = slug
    extension = 1

    while unique_slug in slug_values:
        extension += 1
        unique_slug = f"{slug}-{extension}"

    return unique_slug
