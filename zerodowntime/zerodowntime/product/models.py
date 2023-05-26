from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return self.name
