from django.db.models import Q, Sum, Prefetch, Count
from rest_framework.exceptions import ValidationError

from django.utils import timezone
from datetime import timedelta

from menu.models import Category, MenuRecommendation
from orders.models import Order, NotificationUser
from restaurant.models import Restaurant
from usersApp.models import User, Address
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


class CustomerManager:

    @staticmethod
    def get_admin_login(data):
        username = data.get('username', False)
        password = data.get('password', False)
        if not username or not password:
            raise Exception('Username or Password is required')
        check_user = User.objects.filter(username=username)
        if not check_user:
            raise Exception("No Such User Exist with this username")
        check_pass_db = check_password(password, check_user[0].password)
        if not check_pass_db:
            raise Exception("Username or Password is incorrect")
        return check_user[0]

    @staticmethod
    def get_customer_list(data):
        search = data.get('search', None)

        # Prefetch active addresses only
        active_addresses = Prefetch(
            'addresses',
            queryset=Address.objects.filter(is_active=True),
            to_attr='active_addresses'
        )
        if search:
            users = User.objects.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(phone_number__icontains=search)
            ).annotate(total_orders=Count('order')).prefetch_related(active_addresses)
        else:
            users = User.objects.all().annotate(total_orders=Count('user_order')).prefetch_related(active_addresses)

        return users

    @staticmethod
    def action_customer(data):
        user_id = data.get('userId', False)
        if not user_id:
            raise Exception("UserId is required")
        users = User.objects.filter(id=user_id)
        if users:
            users[0].is_active = not users[0].is_active
            users[0].save()

    @staticmethod
    def get_dashboard_data(data):
        total_orders = Order.objects.count()
        total_revenue = Order.objects.aggregate(total_revenue=Sum('total_amount'))['total_revenue']
        total_customers = User.objects.filter(user_order__isnull=False).distinct().count()
        return {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_customers': total_customers
        }

    @staticmethod
    def get_admin_charts(data):
        total_orders = Order.objects.count()
        on_delivery = Order.objects.filter(status='Ondelivery').count()
        delivered = Order.objects.filter(status='delivered').count()
        cancelled = Order.objects.filter(status='cancelled').count()
        on_delivery_percentage = (on_delivery / total_orders) * 100 if total_orders else 0
        delivered_percentage = (delivered / total_orders) * 100 if total_orders else 0
        cancelled_percentage = (cancelled / total_orders) * 100 if total_orders else 0
        return {
            'on_delivery_percentage':on_delivery_percentage,
            'delivered_percentage':delivered_percentage,
            'cancelled_percentage': cancelled_percentage
        }

    @staticmethod
    def get_rest_status(data):
        is_rest_available = Restaurant.objects.filter()[0].is_open
        return is_rest_available

    @staticmethod
    def change_rest_status(data):
        status = data.get("status", False)
        if not status or status not in ['closed', 'open']:
            raise Exception("status not provided")
        rest_status = Restaurant.objects.filter()[0]
        if status == "closed":
            rest_status.is_open = False
        elif status == "open":
            rest_status.is_open = True
        rest_status.save()

    @staticmethod
    def signup_customer(data):
        full_name = data.get("fullName", False)
        email = data.get("email", False)
        password = data.get("password", False)
        phone = data.get("phone", False)
        passwordConfirm = data.get("passwordConfirm", False)
        if not full_name or not email or not password or not phone or not passwordConfirm:
            raise Exception("Every Field is required")
        if password != passwordConfirm:
            raise Exception("Passwords do not match")
        user_exists = User.objects.filter(Q(email=email) | Q(phone_number=phone)).exists()
        if user_exists:
            raise Exception("Email or Phone already registered")
        user = User.objects.create(full_name=full_name, username=full_name[:3]+email[:3]+phone[:2],email=email, phone_number=phone, password=make_password(password))
        return user

    @staticmethod
    def login_user_customer(data):
        email = data.get('email', False)
        password = data.get('password', False)
        if not email or not password:
            raise Exception('email or Password is required')
        check_user = User.objects.filter(email=email)
        if not check_user:
            raise Exception("No Such User Exist with this username")
        check_pass_db = check_password(password, check_user[0].password)
        if not check_pass_db:
            raise Exception("Username or Password is incorrect")
        return check_user[0]

    @staticmethod
    def fetch_dashboard_data(request, data):
        user = request.user.id
        active_addresses = Prefetch(
            'addresses',
            queryset=Address.objects.filter(is_active=True),
            to_attr='active_addresses'
        )
        req_user = User.objects.filter(id=user).prefetch_related(active_addresses)[0]
        recommended_order = MenuRecommendation.objects.filter()
        all_categories = Category.objects.filter()
        return {
            'req_user': req_user,
            'recommended_order': recommended_order,
            'all_categories':all_categories
        }


    @staticmethod
    def get_customer_address(request, data):
        user = request.user.id
        req_address = Address.objects.filter(user_id=user)
        return req_address

    @staticmethod
    def add_new_customer_address(request, data):
        user = request.user.id
        street = data.get('street', False)
        address = data.get('address', False)
        postalCode = data.get('postalCode', False)
        city = data.get('city', False)
        name = request.data.get('name', False)
        is_active = True
        check_already_address = Address.objects.filter(user_id=user).exists()
        if check_already_address:
            is_active = False
        if not street or  not address or not postalCode or not name or not city:
            raise Exception("Please provide all the details")
        req_address = Address.objects.create(user_id=user, name=name, street=street, zip_code=postalCode, city=city, is_active=is_active)
        return req_address

    @staticmethod
    def delete_customer_address(request, data):
        user = request.user.id
        address_id = data.get('addressId', False)
        if not address_id:
            raise Exception("address id not provided")
        Address.objects.filter(id=address_id, user_id=user).delete()

    @staticmethod
    def change_default_address(request, data):
        user = request.user.id
        address_id = data.get('addressId', False)
        if not address_id:
            raise Exception("address id not provided")
        address = Address.objects.filter(user_id=user).update(is_active=False)
        new_default = Address.objects.get(id=address_id, user_id=user)
        new_default.is_active = True
        new_default.save()

    @staticmethod
    def personal_profile(request, data):
        user = request.user.id
        return User.objects.get(id=user)

    @staticmethod
    def edit_personal_profile(request, data):
        user = request.user.id
        name = data.get('name', False)
        name = data.get('name', False)
        user =  User.objects.get(id=user)


    @staticmethod
    def get_single_customer_detail(data):
        customer_id = data.get('customerId', False)
        if not customer_id:
            raise Exception("Customer id not provided")
        user = User.objects.filter(id=customer_id).prefetch_related("addresses").prefetch_related("user_order", "user_order__order_items")
        return user[0]


    @staticmethod
    def get_notification_user(request, data):
        user_id = request.user.id
        return NotificationUser.objects.filter(user_id=user_id).select_related("order")


    @staticmethod
    def make_password(request, data):
        user_id = data.get("password", False)
        print(make_password(user_id))
