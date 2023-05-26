from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = models.JSONField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return self.name
