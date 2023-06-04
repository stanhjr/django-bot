from django.contrib import admin

from categories.models import Category, SubCategory
from products.models import Product


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 0


class ProductInline(admin.TabularInline):
    model = Product
    fields = ('name', 'code', 'status', 'price')
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
