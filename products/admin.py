from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'tg_nickname')
    search_fields = ('name', 'code')
    list_filter = ('sold_via_bot', 'status')
