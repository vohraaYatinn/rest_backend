from django.db import models
from usersApp.models import User, Address
from menu.models import MenuItem
import uuid
import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class UserCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cart")
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"



class Order(models.Model):
    uuid = models.CharField(max_length=10, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order")
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.IntegerField( default=0)
    status_choices = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('Ondelivery', 'Ondelivery'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')

    def __str__(self):
        return f"Order {self.id} by {self.user}"

    def save(self, *args, **kwargs):
        if not self.uuid:
            # Generate a 10-character UUID
            self.uuid = str(uuid.uuid4())[:10]
        super(Order, self).save(*args, **kwargs)


@receiver(post_save, sender=Order)
def order_saved(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    order_data = {
        'uuid': instance.uuid,
        'user': instance.user.username,
        'status': instance.status,
        'total_amount': str(instance.total_amount),
        'ordered_at': instance.ordered_at.isoformat(),
    }
    async_to_sync(channel_layer.group_send)(
        'orders',
        {
            'type': 'order_update',
            'order': order_data,
        }
    )



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    rating = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.quantity} x {self.item.name}"


class OrderHistory(models.Model):
    order = models.ForeignKey(Order, related_name='order_history', on_delete=models.CASCADE)
    status_choices = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('Ondelivery', 'Ondelivery'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    stamp_at = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return f"{self.order.uuid}"


class AdminNotification(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='admin_notification')
    description = models.TextField()
    stamp_at = models.DateTimeField(auto_now_add=True, null=True)


class NotificationUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_notifications")
    message = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='user_notification_order', null=True)
    stamp_at = models.DateTimeField(auto_now_add=True, null=True)
