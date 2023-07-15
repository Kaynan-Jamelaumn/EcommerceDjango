from django.contrib import admin

from .models import Order, Orders


class OrderAdmin(admin.ModelAdmin):
    list_display = ('variation', 'quantity', 'total',
                    'get_unity_price', 'user', 'created_at')
    list_filter = ('user',)

    def get_unity_price(self, obj):
        return obj.unity_price()
    get_unity_price.short_description = 'Unity Price'


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('address', 'user', 'status', 'total_paid', 'created_at')
    list_filter = ('user', 'status', 'created_at')
    filter_horizontal = ('order',)


admin.site.register(Order, OrderAdmin)
admin.site.register(Orders, OrdersAdmin)
