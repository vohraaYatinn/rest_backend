import re
import random

from django.db.models import Q, Sum, Prefetch, Count
from rest_framework.exceptions import ValidationError

from django.utils import timezone
from datetime import timedelta
import requests
from django.db import transaction

from menu.models import Category, MenuRecommendation, MenuItem
from orders.models import Order, NotificationUser, AdminNotification, UserCart
from restaurant.models import Restaurant
from usersApp.models import User, Address
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.db.models import Case, When, Value, IntegerField


class CustomerManager:

    @staticmethod
    def get_admin_login(data):
        username = data.get('username', False)
        password = data.get('password', False)
        if not username or not password:
            raise Exception('Nome de utilizador ou palavra-passe é obrigatório')
        check_user = User.objects.filter(username=username)
        if not check_user:
            raise Exception("Não existe tal utilizador com este nome de utilizador")
        check_pass_db = check_password(password, check_user[0].password)
        if not check_pass_db:
            raise Exception("Nome de utilizador ou palavra-passe está incorreto")
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
                Q(full_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone_number__icontains=search)
            ).annotate(total_orders=Count('user_order')).prefetch_related(active_addresses)
        else:
            users = User.objects.all().annotate(total_orders=Count('user_order')).prefetch_related(active_addresses)

        return users

    @staticmethod
    def action_customer(data):
        user_id = data.get('userId', False)
        if not user_id:
            raise Exception("O ID do utilizador é obrigatório")
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
            raise Exception("estado não fornecido")
        rest_status = Restaurant.objects.filter()[0]
        if status == "closed":
            rest_status.is_open = False
        elif status == "open":
            rest_status.is_open = True
        rest_status.save()

    @staticmethod
    def signup_customer(data, phone, token):
        full_name = data.get("fullName", False)
        email = data.get("email", False)
        password = data.get("password", False)
        passwordConfirm = data.get("passwordConfirm", False)
        if not full_name or not email or not password or not phone or not passwordConfirm:
            raise Exception("Cada campo é de preenchimento obrigatório")
        if password != passwordConfirm:
            raise Exception("As senhas não coincidem")
        user_exists = User.objects.filter(Q(email=email) | Q(phone_number=phone)).exists()
        if user_exists:
            raise Exception("E-mail ou telefone já registado")
        user = User.objects.create(full_name=full_name, username=full_name[:3]+email[:3]+phone[:2],email=email, phone_number=phone, password=make_password(password))
        if token:
            user.phone_token = token
            user.save()
        return user

    def is_phone_number(value):
        """Check if the value is a valid phone number."""
        phone_regex = r'^\+?\d{9,15}$'  # Simple regex to check phone numbers, adjust as needed
        return re.match(phone_regex, value)

    def is_email(value):
        """Check if the value is a valid email address."""
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # Simple regex to check emails, adjust as needed
        return re.match(email_regex, value)

    @staticmethod
    def login_user_customer(request, data):
        email = data.get('email', False)
        password = data.get('password', False)
        token = request.data.get("token", None)

        if not email or not password:
            raise Exception('e-mail ou palavra-passe é obrigatório')
        # Validate and perform the appropriate query
        if CustomerManager.is_phone_number(email):
            check_user = User.objects.filter(Q(phone_number=email))
        elif CustomerManager.is_email(email):
            check_user = User.objects.filter(Q(email=email))
        else:
            raise ValidationError("Invalid email or phone number format")

        if not check_user:
            raise Exception("Não existe tal utilizador com este nome de utilizador")
        check_pass_db = check_password(password, check_user[0].password)
        if not check_pass_db:
            raise Exception("Nome de utilizador ou palavra-passe está incorreto")
        check_user[0].phone_token = token
        check_user[0].save()
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
        recommended_order = MenuItem.objects.annotate(
                        is_buy_one_priority=Case(
                            When(is_buy_one=True, then=Value(1)),
                            default=Value(0),
                            output_field=IntegerField()
                        )
                    ).order_by('-is_buy_one_priority', '-rating')
        all_categories = Category.objects.filter()
        return {
            'req_user': req_user,
            'recommended_order': recommended_order,
            'all_categories': all_categories
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
            raise Exception("Forneça todos os detalhes")
        req_address = Address.objects.create(user_id=user, name=name, street=street, zip_code=postalCode, city=city, is_active=is_active)
        return req_address

    @staticmethod
    def delete_customer_address(request, data):
        user = request.user.id
        address_id = data.get('addressId', False)
        if not address_id:
            raise Exception("ID de endereço não fornecido")
        Address.objects.filter(id=address_id, user_id=user).delete()

    @staticmethod
    def change_default_address(request, data):
        user = request.user.id
        address_id = data.get('addressId', False)
        if not address_id:
            raise Exception("ID de endereço não fornecido")
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
            raise Exception("ID do cliente não fornecido")
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


    @staticmethod
    def get_notification_fetch():
        return AdminNotification.objects.filter().select_related("order").order_by("-stamp_at")[:10]



    @staticmethod
    def otp_send_phone(data):
        phone = data.get('phone', False)
        if len(phone) != 9:
            raise Exception("Por favor introduza um número de telefone válido")
        if phone == "9999999999":
            return False, False

        url = 'https://cpaas.messagecentral.com/verification/v3/send'
        headers = {
            'authToken': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJDLUFCOTc5QTQzMDU5QzRGMiIsImlhdCI6MTcyNDQxMDEwMSwiZXhwIjoxODgyMDkwMTAxfQ.ViGp17ODCZrEHH9WRcg_x-XPZTjLoffPUSTLxmeg9KCPAiUWxw1wVEkvLjrQ5JD6sPk3QsnoIawmaIkI1870cQ'
        }
        params = {
            'countryCode': '351',
            'customerId': 'C-AB979A43059C4F2',
            'flowType': 'SMS',
            'mobileNumber': phone
        }
        response = requests.post(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("Aguarde 60 segundos antes de tentar novamente.")

        return response.json()['data']['verificationId']

    @staticmethod
    def otp_verify_phone(data):
        phone = data.get('phone', False)
        otp = data.get('otp', False)

        if phone == "9999999999" and otp == "0000":
            check_user = User.objects.filter(phone_number="9999999999")
            return True , check_user[0]

        verfication_code = data.get('verificationCode', False)
        url = 'https://cpaas.messagecentral.com/verification/v3/validateOtp'
        headers = {
            'authToken': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJDLUYwQkMyRUNBNENGOTQ5QiIsImlhdCI6MTczMzY2MTg5NiwiZXhwIjoxODkxMzQxODk2fQ.rxU8zpP5OUZGi3b_A9gjk__cBW1RRegA7eT7mDJR5v2rwjSqTPaExORYlLbNEPQSL6ffqodW4ivZztn0pL0NjA'
        }

        params = {
            'countryCode': '351',
            'mobileNumber': phone,
            'verificationId': verfication_code,
            'customerId': 'C-F0BC2ECA4CF949B',
            'code': otp
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("A OTP é inválida ou está caducada.")
        check_user = User.objects.filter(phone_number=phone)

        return response.json()['data']['verificationStatus'] == 'VERIFICATION_COMPLETED'

    def validate_portuguese_phone_number(phone_number):
        return len(phone_number) == 9

    @staticmethod
    @transaction.atomic
    def signup_user(data):
        phone = data['inputValues'].get('phone', False)
        if CustomerManager.validate_portuguese_phone_number(phone) is False:
            raise Exception("O número de telefone não é válido")
        user_check = User.objects.filter(phone_number=phone)
        if user_check:
            raise ValidationError("Phone Number already exist")
        url = 'https://cpaas.messagecentral.com/verification/v3/send'
        headers = {
            'authToken': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJDLUYwQkMyRUNBNENGOTQ5QiIsImlhdCI6MTczMzY2MTg5NiwiZXhwIjoxODkxMzQxODk2fQ.rxU8zpP5OUZGi3b_A9gjk__cBW1RRegA7eT7mDJR5v2rwjSqTPaExORYlLbNEPQSL6ffqodW4ivZztn0pL0NjA'
        }
        params = {
            'countryCode': '351',
            'customerId': 'C-F0BC2ECA4CF949B',
            'flowType': 'SMS',
            'mobileNumber': phone
        }
        response = requests.post(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("Aguarde 60 segundos antes de tentar novamente.")

        return response.json(), phone

    @staticmethod
    @transaction.atomic
    def initiate_payment_mbway(request, data):
        mobile_number = data['inputValues'].get("phone", False)
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
        total_amount = 0
        for cart_item in cart_items:
            if cart_item.item.is_buy_one:
                payable_quantity = cart_item.quantity - min(cart_item.quantity // 2, 1)
            else:
                payable_quantity = cart_item.quantity

            total_amount += payable_quantity * cart_item.item.price

        total_amount = round(total_amount, 2)

        url = "https://api.ifthenpay.com/spg/payment/mbway"

        # Parameters to be sent in the POST request
        payload = {
                "mbWayKey": "RLA-844371",
                "orderId": f"{cart_items[0].id}-{random.randint(1000, 9999)}",  # Adding random 4-digit number
                "amount": float(total_amount),
                "mobileNumber": f"351#{mobile_number}",
                "description": "order for rest"
            }

        headers = {"Content-Type": "application/json"}

        # Sending the POST request with JSON payload
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        if response_json.get('Message', False) == "Success" and response_json.get('RequestId', False):
            cart_items.update(verification_number = response_json['RequestId'])
        return response_json

    @staticmethod
    @transaction.atomic
    def check_payment_mbway(data):
        verification_id = data.get("verificationId", False)

        url = "https://api.ifthenpay.com/spg/payment/mbway/status"

        # Parameters to be sent in the POST request
        params = {
              "mbWayKey": "RLA-844371",
              "requestId": verification_id
            }

        headers = {"Content-Type": "application/json"}

        # Sending the POST request with JSON payload
        response = requests.get(url, headers=headers, params=params)
        return response.json()



    @staticmethod
    @transaction.atomic
    def forgot_password_otp_send(data):
        phone = data['inputValues'].get('phone', False)
        if CustomerManager.validate_portuguese_phone_number(phone) is False:
            raise Exception("O número de telefone não é válido")
        user_check = User.objects.filter(phone_number=phone)
        if not user_check:
            raise ValidationError("no account is associated with this phone number")
        url = 'https://cpaas.messagecentral.com/verification/v3/send'
        headers = {
            'authToken': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJDLUYwQkMyRUNBNENGOTQ5QiIsImlhdCI6MTczMzY2MTg5NiwiZXhwIjoxODkxMzQxODk2fQ.rxU8zpP5OUZGi3b_A9gjk__cBW1RRegA7eT7mDJR5v2rwjSqTPaExORYlLbNEPQSL6ffqodW4ivZztn0pL0NjA'
        }
        params = {
            'countryCode': '351',
            'customerId': 'C-F0BC2ECA4CF949B',
            'flowType': 'SMS',
            'mobileNumber': phone
        }
        response = requests.post(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("Aguarde 60 segundos antes de tentar novamente.")

        return response.json(), phone


    @staticmethod
    def change_password_after_forgot(data, phone):
        password = data.get("password", False)
        passwordConfirm = data.get("passwordConfirm", False)
        if not password or not passwordConfirm:
            raise Exception("Cada campo é de preenchimento obrigatório")
        if password != passwordConfirm:
            raise Exception("As senhas não coincidem")
        user_exists = User.objects.filter(Q(phone_number=phone))
        if not user_exists:
            raise Exception("There is some error please try again later")
        user_exists[0].password = make_password(password)
        user_exists[0].save()
