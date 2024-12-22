from rest_framework import serializers

from usersApp.models import Address, User
from usersApp.serializers import UserSerializer
from .models import Order, OrderItem, OrderHistory, UserCart
from menu.serializers import MenuItemSerializer


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    item = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"

class OrderSerializerWithUser(serializers.ModelSerializer):
    address = AddressSerializer()
    order_items = OrderItemSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Order
        fields = "__all__"

class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = "__all__"


class OrderAllDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressSerializer()
    order_items = OrderItemSerializer(many=True)
    order_history = OrderHistorySerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"


class UserCartSerializer(serializers.ModelSerializer):
    item = MenuItemSerializer()

    class Meta:
        model = UserCart
        fields = "__all__"
