from django.contrib import admin

from stocks.models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass
