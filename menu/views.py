from rest_framework import viewsets

from .manager import MenuManager
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer, MenuItemCategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class DeleteCategoryView(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data
            MenuManager.delete_category(data)
            return Response({"result" : "success", "message":"Category deleted successfully"}, 200)

        except Exception as err:
            return Response(str(err), 500)

class CategoryView(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.data
            get_category_list = MenuManager.get_category(data)
            serialized_data = CategorySerializer(get_category_list, many=True).data
            return Response({"result" : "success", "data":serialized_data}, 200)

        except Exception as err:
            return Response(str(err), 500)

    @staticmethod
    def post(request):
        try:
            data = request.data
            MenuManager.add_category(data)
            return Response({"result" : "success", "message":"Category added successfully"}, 200)

        except Exception as err:
            return Response(str(err), 500)



class MenuView(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            get_category_list = MenuManager.get_category(data)
            return Response({"result" : "success", "message":"login successfull", "login":check_lgoin}, 200)

        except Exception as err:
            return Response(str(err), 500)

    @staticmethod
    def post(request):
        try:
            data = request.data
            MenuManager.add_menu_item(data)
            return Response({"result" : "success", "message":"Menu Item added successfully"}, 200)

        except Exception as err:
            return Response(str(err), 500)


class ChangeAvailablity(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data
            change_availability = MenuManager.change_avail_menu(data)
            return Response({"result" : "success", "message":"Status of the item changed successfully"}, 200)

        except Exception as err:
            return Response(str(err), 500)


class SingleMenuItem(APIView):

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            menu_item = MenuManager.get_single_menu_item(data)
            serialized_data = MenuItemCategorySerializer(menu_item).data
            return Response({"result" : "success", "data":serialized_data}, 200)

        except Exception as err:
            return Response(str(err), 500)

class fetchAllMenuItems(APIView):

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            menu_item = MenuManager.fetch_all_menu_items(data)
            serialized_data = MenuItemCategorySerializer(menu_item, many=True).data
            return Response({"result" : "success", "data":serialized_data}, 200)

        except Exception as err:
            return Response(str(err), 500)


class fetchMenuByCategory(APIView):

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            menu_item = MenuManager.search_by_category(data)
            serialized_data = MenuItemCategorySerializer(menu_item, many=True).data
            return Response({"result" : "success", "data":serialized_data}, 200)

        except Exception as err:
            return Response(str(err), 500)


class checkRestOnline(APIView):

    @staticmethod
    def get(request):
        try:
            check_rest = MenuManager.rest_offline_online_check()
            return Response({"result" : "success", "data":check_rest}, 200)

        except Exception as err:
            return Response(str(err), 500)



class getAllSideItems(APIView):

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            menu_item = MenuManager.get_all_side_items(data)
            serialized_data = MenuItemCategorySerializer(menu_item, many=True).data
            return Response({"result" : "success", "data":serialized_data}, 200)

        except Exception as err:
            return Response(str(err), 500)




class ChangeOneBuyOne(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data
            change_availability = MenuManager.change_buy_one_get_one(data)
            return Response({"result" : "success", "message":"Status of the item changed successfully"}, 200)

        except Exception as err:
            return Response(str(err), 500)




class ChangeToAddonlist(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data
            change_availability = MenuManager.change_is_add_on(data)
            return Response({"result" : "success", "message":"Status of the item changed successfully"}, 200)

        except Exception as err:
            return Response(str(err), 500)
