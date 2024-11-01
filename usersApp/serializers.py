from rest_framework import serializers

from menu.models import MenuItem
from orders.models import Order, OrderItem, NotificationUser
from .models import User, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'zip_code']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserAddressSerializer(serializers.ModelSerializer):
    active_addresses = AddressSerializer(many=True)
    total_orders = serializers.IntegerField()
    class Meta:
        model = User
        fields = "__all__"


class UserOnlyAddressSerializer(serializers.ModelSerializer):
    active_addresses = AddressSerializer(many=True)
    class Meta:
        model = User
        fields = "__all__"


class AddressUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"


class OrdersItemSerializer(serializers.ModelSerializer):
    item = MenuItemSerializer()
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrdersSerializer(serializers.ModelSerializer):
    order_items = OrdersItemSerializer(many=True)
    class Meta:
        model = Order
        fields = "__all__"


class UserSingleSerializer(serializers.ModelSerializer):
    addresses = AddressUserSerializer(many=True)
    user_order = OrdersSerializer(many=True)

    class Meta:
        model = User
        fields = "__all__"

class getNotificationSerializer(serializers.ModelSerializer):
    order = OrdersSerializer()

    class Meta:
        model = NotificationUser
        fields = "__all__"
