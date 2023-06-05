from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_categories')

    def get_all_products_count(self):
        product_count = self.products.count()
        for sub_category in self.sub_categories.all():
            product_count += sub_category.get_all_products_count()

        return product_count

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.name}'
        return f'{self.name}'


class SubCategory(Category):
    class Meta:
        proxy = True
