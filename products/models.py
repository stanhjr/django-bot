import os

from django.db import models

from categories.models import SubCategory


class Product(models.Model):
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('available', 'Available'),
        ('sold', 'Sold'),
    ]
    sub_category = models.ForeignKey(
        SubCategory,
        related_name='products',
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='available')
    code = models.BigIntegerField()
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=5000)
    image = models.ImageField(upload_to='product_images')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    sold_via_bot = models.BooleanField(blank=True, null=True)

    @property
    def image_url(self):
        return f'{os.environ.get("HOSTNAME")}/{self.image}'

    def __str__(self):
        return f'Product {self.name}'
