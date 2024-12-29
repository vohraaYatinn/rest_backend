from django.db import transaction
from django.db.models import Q, Sum, F
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg
from django.db import transaction
from django.db.models import F, Sum
from restaurant.models import Restaurant
from usersApp.models import Address, User
from .firebaseSdk import send_notification
from .models import Order, OrderHistory, UserCart, OrderItem, NotificationUser, AdminNotification


class OrderManager:

    @staticmethod
    def add_user_notification(user, message, order=False):
        notification = NotificationUser.objects.create(user_id=user, message=message)
        notification.order = order
        notification.save()

    @staticmethod
    def order_fetch(data):
        day = data.get("day[label]", False)
        date = data.get("date", False)
        if day == False:
            day = "Today"
        query = Q()

        if date:
            query = Q(ordered_at__date=date)

        elif day == "Today":
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
        orders = Order.objects.filter(payment_status="success").select_related("address").prefetch_related("order_items", "order_items__item").select_related("user").filter(query).order_by("-ordered_at")
        return orders

    @staticmethod
    @transaction.atomic
    def order_status_change(data):
        order_id = data.get("uuid", False)
        status = data.get("status", False)

        if not order_id or not status:
            raise Exception("order_id ou status é obrigatório")

        orders = Order.objects.filter(uuid=order_id)
        if not orders:
            raise Exception("o ID do pedido é inválido")
        if orders[0].status == status:
            raise Exception("o estado do pedido já está atualizado")
        orders[0].status = status
        if not orders[0].is_attended:
            orders[0].is_attended = True
        orders[0].save()
        OrderHistory.objects.create(order=orders[0], status=status)
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('Ondelivery', 'Ondelivery'),
        message = ""
        admin_message = ""
        if status == "accepted":
            message = "Your Order has been accepted"
            admin_message = f"Order #{orders[0].uuid} has been accepted"
        elif status == "delivered":
            message = "The Order has been delivered"
            admin_message = f"Order #{orders[0].uuid} has been delivered"
        elif status == "cancelled":
            message = "The Order has been cancelled"
            admin_message = f"Order #{orders[0].uuid} has been cancelled"
        elif status == "Ondelivery":
            message = "The Order has been out for delivery"
            admin_message = f"Order #{orders[0].uuid} has been Ondelivery"

        NotificationUser.objects.create(user=orders[0].user,message=message ,order=orders[0])
        AdminNotification.objects.create(order=orders[0], description=admin_message)
        return orders

    @staticmethod
    def single_order_details(data):
        order_uuid = data.get("uuid", False)
        query = Q()
        query &= Q(uuid=order_uuid) | Q(id=order_uuid)
        if not order_uuid:
            raise Exception("order_id é obrigatório")
        orders = Order.objects.filter(query).select_related("user","address").prefetch_related("order_items", "order_items__item", "order_history")
        return orders

    @staticmethod
    def add_to_cart(request, data):
        user_id = request.user.id
        menu = data.get("menuId", False)
        quantity = data.get("quantity", False)
        if not menu or not quantity:
            raise Exception("order_id é obrigatório")
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

        total_amount = 0
        for item in cart_items:
            if item.item.is_buy_one:
                payable_quantity = item.quantity - min(item.quantity // 2, 1)
            else:
                payable_quantity = item.quantity
            total_amount += payable_quantity * item.item.price

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
            raise Exception("Há algo de errado com o seu carrinho")
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
    @transaction.atomic
    def check_order_before_payment(request, data):
        # Check if the restaurant is online
        check_rest_online = Restaurant.objects.first()
        if not check_rest_online.is_open:
            raise Exception("A loja está offline.")

        user_id = request.user.id

        # Fetch active address
        address = Address.objects.filter(user_id=user_id, is_active=True)
        if not address.exists():
            raise Exception("Nenhum endereço ativo encontrado para o utilizador")

        # Fetch cart items with related item details
        cart_items = UserCart.objects.filter(user_id=user_id).select_related("item")
        if not cart_items.exists():
            raise Exception("O carrinho está vazio. Por favor adicione artigos ao seu carrinho")

        # Check for unavailable items in the cart
        is_change_in_cart = False
        for item in cart_items:
            if not item.item.is_available:
                is_change_in_cart = True
                item.delete()  # Remove unavailable item from the cart

        if is_change_in_cart:
            raise Exception(
                "Some items in your cart were not available and have been removed. Please review your cart.")

        # Calculate total amount with "Buy 1 Get 1 Free" logic

        # total_amount = 0
        # for cart_item in cart_items:
        #     if cart_item.item.is_buy_one:
        #         # Payable quantity after considering free items
        #         payable_quantity = cart_item.quantity - min(cart_item.quantity // 2, 1)
        #     else:
        #         payable_quantity = cart_item.quantity
        #
        #     # Add item total to the total amount
        #     total_amount += payable_quantity * cart_item.item.price
        #
        # total_amount = round(total_amount, 2)
        #
        # # Create the Order
        # order = Order.objects.create(
        #     user_id=user_id,
        #     address=address[0],
        #     total_amount=total_amount
        # )
        #
        # # Add items to the Order
        # for cart_item in cart_items:
        #     if cart_item.item.is_buy_one:
        #         # Payable quantity after considering free items
        #         payable_quantity = cart_item.quantity - min(cart_item.quantity // 2, 1)
        #     else:
        #         payable_quantity = cart_item.quantity
        #
        #     OrderItem.objects.create(
        #         order=order,
        #         item=cart_item.item,
        #         quantity=payable_quantity,
        #         price=cart_item.item.price
        #     )
        #
        # # Clear the user's cart after placing the order
        # UserCart.objects.filter(user_id=user_id).delete()
        #
        # # Log the order in OrderHistory
        # OrderHistory.objects.create(order=order)
        #
        # # Notify the user about the successful order
        # OrderManager.add_user_notification(user_id, "Order placed successfully", order=order)


    @staticmethod
    @transaction.atomic
    def check_order_after_payment(request, data):
        verification_id = data.get("verificationId", False)
        user_id = request.user.id
        order = Order.objects.get(
            payment_reference_number=verification_id
        )
        order.payment_status = "success"
        order.save()
        UserCart.objects.filter(user_id=user_id).delete()
        # Log the order in OrderHistory
        OrderHistory.objects.create(order=order)
        # Notify the user about the successful order
        OrderManager.add_user_notification(user_id, "Pedido realizado com sucesso", order=order)


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
            query).filter(payment_status="success").order_by("-ordered_at")

    @staticmethod
    @transaction.atomic()
    def change_order_attended(data):
        order = data.get("uuid", False)
        if not order:
            raise Exception("Order id is invalid")
        Order_obj = Order.objects.filter(id=order)
        if not Order_obj:
            raise Exception("Order id is invalid")
        Order_obj[0].is_attended = True
        Order_obj[0].save()

    @staticmethod
    @transaction.atomic
    def order_status_change(data):
        order_id = data.get("uuid", False)
        status = data.get("status", False)

        if not order_id or not status:
            raise Exception("order_id ou status é obrigatório")

        orders = Order.objects.filter(uuid=order_id)
        if not orders:
            raise Exception("o ID do pedido é inválido")
        if orders[0].status == status:
            raise Exception("o estado do pedido já está atualizado")
        orders[0].status = status
        if not orders[0].is_attended:
            orders[0].is_attended = True
        orders[0].save()
        OrderHistory.objects.create(order=orders[0], status=status)
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('Ondelivery', 'Ondelivery'),
        message = ""
        admin_message = ""
        if status == "accepted":
            message = "Your Order has been accepted"
            admin_message = f"Order #{orders[0].uuid} has been accepted"
        elif status == "delivered":
            message = "The Order has been delivered"
            admin_message = f"Order #{orders[0].uuid} has been delivered"
        elif status == "cancelled":
            message = "The Order has been cancelled"
            admin_message = f"Order #{orders[0].uuid} has been cancelled"
        elif status == "Ondelivery":
            message = "The Order has been out for delivery"
            admin_message = f"Order #{orders[0].uuid} has been Ondelivery"

        NotificationUser.objects.create(user=orders[0].user,message=message ,order=orders[0])
        AdminNotification.objects.create(order=orders[0], description=admin_message)
        return orders
