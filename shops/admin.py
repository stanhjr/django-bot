from django.contrib import admin

from shops.models import City, Address


class AddressInline(admin.TabularInline):
    model = Address
    fields = ('address_name', 'google_map_link')
    extra = 0


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    inlines = [AddressInline, ]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
