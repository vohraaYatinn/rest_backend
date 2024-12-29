from .models import Order, OrderItem, OrderHistory, NotificationUser, UserCart, AdminNotification
from django.contrib import admin


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ordered_at', 'total_amount', 'status', 'rating', 'is_attended', 'payment_status')  # Include datetime field
    fields = ('user', 'address', 'ordered_at', 'total_amount', 'status', 'is_attended')  # Fields to display in the detail view
    readonly_fields = ('ordered_at', 'uuid')  # Make these fields read-only if necessary

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(OrderHistory)
admin.site.register(NotificationUser)
admin.site.register(UserCart)
admin.site.register(AdminNotification)
