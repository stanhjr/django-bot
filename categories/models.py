from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        related_name='sub_categories',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name}'


