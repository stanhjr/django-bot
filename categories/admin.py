from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from categories.models import Category, SubCategory
from products.models import Product


class SubCategoryInline(admin.TabularInline):
    model = Category
    extra = 0

    readonly_fields = ('view_category',)

    def view_category(self, instance):
        url = reverse('admin:categories_subcategory_change', args=[instance.id])
        return format_html('<a href="{}">{}</a>', url, instance.name)

    view_category.short_description = 'View Category'


class ProductInline(admin.TabularInline):
    model = Product
    fields = ('name', 'code', 'status', 'price')
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline, ProductInline]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=True)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline, ProductInline]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=False)

