from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Cart, Order, OrderItem, FailedOrder


admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)

class FailedOrderAdmin(admin.ModelAdmin):
    list_display = ('order_display', 'product', 'quantity','total_price', 'refund_button')

    
    def order_display(self, obj):
        url = reverse('admin:cart_order_change', args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', url, obj.order)
    order_display.short_description = "Order"

    
    def total_price_display(self, obj):
        return f"${obj.total_price:.2f}"
    total_price_display.short_description = "Total Price"

    
    def short_shipping_response(self, obj):
        return f"{obj.shipping_response[:50]}..." if len(obj.shipping_response) > 50 else obj.shipping_response
    short_shipping_response.short_description = "Shipping Response"

    
    def refund_button(self, obj):
        return format_html(
            '<a class="button" href="{}" style="background-color: 
            f"/cart/failed-order/{obj.id}/refund"
        )
    refund_button.short_description = "Refund Action"

    
    class Media:
        css = {
            'all': ('admin/css/custom.css',),
        }


admin.site.register(FailedOrder, FailedOrderAdmin)
