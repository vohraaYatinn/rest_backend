from django.db.models import Q
from rest_framework.exceptions import ValidationError

from django.utils import timezone
from datetime import timedelta

from menu.models import Category, MenuItem


class MenuManager:

    @staticmethod
    def get_category(data):
        category = Category.objects.filter().prefetch_related("items")
        return category

    @staticmethod
    def add_category(data):
        category_name = data.get("name")
        if not category_name:
            raise Exception("Category name is required")
        category = Category.objects.filter(name=category_name)
        if category.exists():
            raise Exception("Category already exists")
        Category.objects.create(name=category_name)

    @staticmethod
    def delete_category(data):
        category_id = data.get("id")
        if not category_id:
            raise Exception("Category id is required")
        Category.objects.filter(id=category_id).delete()

    @staticmethod
    def change_avail_menu(data):
        id = data.get("id", False)
        action = data.get("action", False)
        if not id or not action:
            raise Exception("id and action are required")
        bool_flag = False
        if action == "available":
            bool_flag = True
        menu_item = MenuItem.objects.filter(id=id)
        if menu_item:
            menu_item[0].is_available = bool_flag
            menu_item[0].save()

    @staticmethod
    def add_menu_item(data):
        name = data.get("ProductName", False)
        description = data.get("Description", False)
        price = data.get("Price", False)
        category = data.get("Category", False)
        img = data.get("img", False)
        if not name or not description or not price or not category or not img:
            raise Exception ("All Fields are required")
        category_id = Category.objects.get(name=category)
        MenuItem.objects.create(category=category_id, name=name, description=description, price=price, image=img)


    @staticmethod
    def get_single_menu_item(data):
        menu_id = data.get("menuId", False)
        if not menu_id:
            raise Exception("menuId is required")
        return MenuItem.objects.get(id=menu_id)

    @staticmethod
    def fetch_all_menu_items(data):
        search = data.get("search", False)
        query = Q(is_available=True)
        if search:
            query &= Q(name__icontains=search)
        return MenuItem.objects.filter(query).select_related("category")

    @staticmethod
    def search_by_category(data):
        category_id = data.get("categoryId", False)
        query = Q(is_available=True)
        if category_id:
            query &= Q(category_id=category_id)
        return MenuItem.objects.filter(query).select_related("category")