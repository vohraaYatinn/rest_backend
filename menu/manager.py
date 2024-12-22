from django.db.models import Q
from rest_framework.exceptions import ValidationError

from django.utils import timezone
from datetime import timedelta

from menu.models import Category, MenuItem
from restaurant.models import Restaurant


class MenuManager:

    @staticmethod
    def get_category(data):
        category = Category.objects.filter().prefetch_related("items")
        return category

    @staticmethod
    def add_category(data):
        category_name = data.get("name")
        if not category_name:
            raise Exception("O nome da categoria é obrigatório")
        category = Category.objects.filter(name=category_name)
        if category.exists():
            raise Exception("A categoria já existe")
        Category.objects.create(name=category_name)

    @staticmethod
    def delete_category(data):
        category_id = data.get("id")
        if not category_id:
            raise Exception("O ID da categoria é obrigatório")
        Category.objects.filter(id=category_id).delete()

    @staticmethod
    def change_avail_menu(data):
        id = data.get("id", False)
        action = data.get("action", False)
        if not id or not action:
            raise Exception("id e ação são necessários")
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
            raise Exception("O menuId é obrigatório")
        return MenuItem.objects.select_related("category").get(id=menu_id)

    @staticmethod
    def fetch_all_menu_items(data):
        search = data.get("search", False)
        query = Q()
        if search:
            query &= Q(name__icontains=search)
        return MenuItem.objects.filter(query).select_related("category")

    @staticmethod
    def get_all_side_items(data):
        return MenuItem.objects.filter(side_on=True).select_related("category")

    @staticmethod
    def search_by_category(data):
        category_id = data.get("categoryId", False)
        query = Q()
        if category_id:
            query &= Q(category_id=category_id)
        return MenuItem.objects.filter(query).select_related("category")

    @staticmethod
    def rest_offline_online_check():
        return Restaurant.objects.filter()[0].is_open


    @staticmethod
    def change_buy_one_get_one(data):
        id = data.get("id", False)
        if not id:
            raise Exception("a identificação é obrigatória")
        menu_item = MenuItem.objects.filter(id=id)
        if menu_item:
            menu_item[0].is_buy_one = not menu_item[0].is_buy_one
            menu_item[0].save()


    @staticmethod
    def change_is_add_on(data):
        id = data.get("id", False)
        if not id:
            raise Exception("a identificação é obrigatória")
        menu_item = MenuItem.objects.filter(id=id)
        if menu_item:
            menu_item[0].side_on = not menu_item[0].side_on
            menu_item[0].save()


    @staticmethod
    def edit_menu_item(data):
        id = data.get("id", False)
        name = data.get("ProductName", False)
        description = data.get("Description", False)
        price = data.get("Price", False)
        category = data.get("Category", False)
        img = data.get("img", False)
        menu_items = MenuItem.objects.filter(id=id)
        if not menu_items:
            raise Exception("Item de menu não encontrado")
        if name:
            menu_items[0].name = name
        if description:
            menu_items[0].description = description
        if price:
            menu_items[0].price = price
        if category:
            category_id = Category.objects.get(name=category)
            menu_items[0].category_id = category_id
        if img:
            menu_items[0].image = img
        menu_items[0].save()