import sys
from django.utils import timezone

sys.path.insert(0, '../../')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_backend.settings')
import django
import requests
django.setup()

from orders.models import Order, UserCart, OrderItem, OrderHistory, NotificationUser, ScriptMessage
from usersApp.models import Address
today = timezone.now().date()

message_to_print = ""
counter = 0
try:
    fetch_all_cart = UserCart.objects.filter(verification_number__isnull=False)
    unique_verification_list = fetch_all_cart.values_list('verification_number', flat=True).distinct()
    for unique_number in unique_verification_list:
        try:
            verification_id = unique_number
            url = "https://api.ifthenpay.com/spg/payment/mbway/status"
            params = {
                    "mbWayKey": "RLA-844371",
                    "requestId": verification_id
                }
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers, params=params)
            response = response.json()
            if response['Message'] == "Success":
                cart_items = UserCart.objects.filter(verification_number=verification_id).select_related("item")
                user = cart_items[0].user
                address = Address.objects.filter(user=user, is_active=True)
                total_amount = 0
                order = Order.objects.create(
                    user=user,
                    address=address[0],
                    total_amount=0
                )
                for cart_item in cart_items:
                    if cart_item.item.is_buy_one:
                        payable_quantity = cart_item.quantity - min(cart_item.quantity // 2, 1)
                    else:
                        payable_quantity = cart_item.quantity
                    OrderItem.objects.create(
                        order=order,
                        item=cart_item.item,
                        quantity=payable_quantity,
                        price=cart_item.item.price
                    )
                    total_amount += payable_quantity * cart_item.item.price
                total_amount = round(total_amount, 2)
                order.total_amount = total_amount
                order.save()
                cart_items.delete()
                OrderHistory.objects.create(order=order)
                notification = NotificationUser.objects.create(user=user, message="Pedido realizado com sucesso")
                notification.order = order
                notification.save()
                counter = counter + 1
            elif response['Message'] == "Failed" or response['Message'] == "Expired" or response['Message'] == "Declined by user":        
                UserCart.objects.filter(verification_number=verification_id).update(verification_number=None)
        except:
            pass
    message_to_print = f"Edit on {counter}"
    status = "success"
except Exception as e:
    message_to_print = "Edit on error"
    status = "fail"

ScriptMessage.objects.create(
    message=message_to_print,
    status=status
)
if ScriptMessage.objects.count() > 100:
    # Get IDs of the records to delete
    excess_records = ScriptMessage.objects.order_by('-id')[100:]
    ScriptMessage.objects.filter(id__in=[record.id for record in excess_records]).delete()