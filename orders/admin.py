from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'full_name', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'full_name', 'phone', 'user__username')
    readonly_fields = ('order_number', 'user', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'user', 'status', 'created_at', 'updated_at')
        }),
        ('Customer Details', {
            'fields': ('full_name', 'email', 'phone', 'address')
        }),
        ('Payment & Delivery', {
            'fields': ('payment_method', 'total_price', 'estimated_delivery')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'price')
    list_filter = ('order__created_at',)
    search_fields = ('order__order_number', 'item__name')
    readonly_fields = ('order', 'item', 'price')

