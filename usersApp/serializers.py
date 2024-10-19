from rest_framework import serializers
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
