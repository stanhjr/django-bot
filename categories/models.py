from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_categories')

    def get_all_products_count(self):
        product_count = self.products.count()
        for sub_category in self.sub_categories.all():
            product_count += sub_category.get_all_products_count()

        return product_count

    def get_all_sale_out_products_count(self):
        product_count = self.products.filter(sale_out=True).count()
        for sub_category in self.sub_categories.all():
            product_count += sub_category.get_all_sale_out_products_count()
        return product_count

    @property
    def parent_category_for_bot(self):
        if self.parent:
            if self.parent.parent:
                return self.parent.parent.id

    @property
    def count_parents(self):
        count = 0
        current_category = self

        while current_category.parent:
            count += 1
            current_category = current_category.parent

        return count

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.name}'
        return f'{self.name}'


class SubCategory(Category):
    class Meta:
        proxy = True
