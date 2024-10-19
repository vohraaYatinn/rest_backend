from django.db import transaction
from django.db.models import Q, Sum, F
from django.utils import timezone
from datetime import timedelta

from usersApp.models import Address
from .models import Order, OrderHistory, UserCart, OrderItem


class OrderManager:

    @staticmethod
    def order_fetch(data):
        day = data.get("day[label]", False)
        if day == False:
            day = "Today"
        query = Q()

        if day == "Today":
            # Get the start and end of today
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
            query &= Q(ordered_at__range=(today_start, today_end))

        elif day == "Yesterday":
            # Get the start and end of yesterday
            yesterday_start = (timezone.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            yesterday_end = (timezone.now() - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)
            query &= Q(ordered_at__range=(yesterday_start, yesterday_end))

        # Fetch the orders based on the query
        orders = Order.objects.select_related("address").prefetch_related("order_items", "order_items__item").filter(query).order_by("-ordered_at")
        return orders

    @staticmethod
    @transaction.atomic
    def order_status_change(data):
        order_id = data.get("uuid", False)
        status = data.get("status", False)

        if not order_id or not status:
            raise Exception("order_id or status is required")

        orders = Order.objects.filter(uuid=order_id)
        if not orders:
            raise Exception("order id is invalid")
        if orders[0].status == status:
            raise Exception("order status is already updated")
        orders[0].status = status
        orders[0].save()
        OrderHistory.objects.create(order=orders[0], status=status)

        return orders

    @staticmethod
    def single_order_details(data):
        order_uuid = data.get("uuid", False)
        query = Q()
        query &= Q(uuid=order_uuid) | Q(id=order_uuid)
        if not order_uuid:
            raise Exception("order_id is required")
        orders = Order.objects.filter(query).select_related("user","address").prefetch_related("order_items", "order_items__item", "order_history")
        return orders

    @staticmethod
    def add_to_cart(request, data):
        user_id = request.user.id
        menu = data.get("menuId", False)
        quantity = data.get("quantity", False)
        if not menu or not quantity:
            raise Exception("order_id is required")
        item = UserCart.objects.filter(user_id=user_id, item_id=menu)
        if item:
            item[0].quantity += quantity
            item[0].save()
        else:
            UserCart.objects.create(user_id=user_id,item_id=menu, quantity=quantity)

    @staticmethod
    def fetch_cart(request, data):
        user_id = request.user.id
        cart_items = UserCart.objects.filter(user_id=user_id)
        total_amount = cart_items.aggregate(
            total=Sum(F('quantity') * F('item__price'))
        )['total'] or 0
        total_amount = round(total_amount, 2)
        address = Address.objects.filter(user_id=user_id, is_active=True)
        return cart_items, total_amount, address

    @staticmethod
    def cart_action(request, data):
        user_id = request.user.id
        cart_id = data.get("id", False)
        action = data.get("action", False)
        cart = UserCart.objects.filter(id=cart_id, user_id=user_id)
        if not cart:
            raise Exception("There is something issue with your cart")
        if action == "decrement":
            cart[0].quantity = cart[0].quantity - 1
            if cart[0].quantity == 0:
                cart[0].delete()
            else:
                cart[0].save()

        elif action == "increment":
            cart[0].quantity = cart[0].quantity + 1
            cart[0].save()
        elif action == "delete":
            cart[0].delete()

    @staticmethod
    @transaction.atomic()
    def place_order(request, data):
        user_id = request.user.id
        address = Address.objects.filter(user_id=user_id, is_active=True)
        cart_items = UserCart.objects.filter(user_id=user_id)
        total_amount = cart_items.aggregate(
            total=Sum(F('quantity') * F('item__price'))
        )['total'] or 0
        total_amount = round(total_amount, 2)
        order = Order.objects.create(user_id=user_id, address=address[0], total_amount=total_amount)
        for items in cart_items:
            OrderItem.objects.create(order=order, item=items.item, quantity=items.quantity)
        UserCart.objects.filter(user_id=user_id).delete()
        OrderHistory.objects.create(order=order)

    @staticmethod
    def get_orders_customer(request, data):
        user_id = request.user.id
        status = data.get("status", False)
        query = Q()
        query &= Q(user_id=user_id)
        if status == "ongoing":
            query &= Q(status = "pending") | Q(status = "accepted") | Q(status = "Ondelivery")
        elif status == "history":
            query &= Q(status = "delivered") | Q(status = "cancelled")
        return Order.objects.select_related("address").prefetch_related("order_items", "order_items__item").filter(
            query).order_by("-ordered_at")