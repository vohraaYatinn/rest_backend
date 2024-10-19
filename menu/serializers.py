from rest_framework import serializers
from .models import Category, MenuItem, MenuRecommendation


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"


class MenuRecommendationSerializer(serializers.ModelSerializer):
    menu = MenuItemSerializer()
    class Meta:
        model = MenuRecommendation
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)

    class Meta:
        model = Category
        fields = "__all__"


class CategoryOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"



class MenuItemCategorySerializer(serializers.ModelSerializer):
    category = CategoryOnlySerializer()
    class Meta:
        model = MenuItem
        fields = "__all__"