from django.contrib import admin
from .models import Product, Order


admin.site.register(Product)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'name',
        'phone',
        'total',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'name',
        'phone',
        'user__username',
    )