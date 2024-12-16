from rest_framework import viewsets

from usersApp.custom_permission import IsUserAuth
from .manager import OrderManager
from .models import Order
from .serializers import OrderSerializer, OrderItemSerializer, OrderAllDetailsSerializer, UserCartSerializer, \
    AddressSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class OrderView(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            order_details = OrderManager.order_fetch(data)
            serializer_data = OrderSerializer(order_details, many=True).data
            return Response({"result" : "success", "data":serializer_data}, 200)

        except Exception as err:
            return Response(str(err), 500)

class OrderStatusChange(APIView):
    @staticmethod
    def post(request):
        try:
            data = request.data
            order_details = OrderManager.order_status_change(data)
            return Response({"result" : "success", "message":"status changed successfully"}, 200)

        except Exception as err:
            return Response(str(err), 500)


class FetchSingleOrder(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            order_details = OrderManager.single_order_details(data)
            serializer_data = OrderAllDetailsSerializer(order_details, many=True).data
            return Response({"result" : "success", "data":serializer_data}, 200)

        except Exception as err:
            return Response(str(err), 500)



class AddToCart(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def post(request):
        try:
            data = request.data
            OrderManager.add_to_cart(request, data)
            return Response({"result" : "success", "message":"Item added successfully"}, 200)

        except Exception as err:
            return Response(str(err), 500)

class FetchCustomerCart(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def get(request):
        try:
            data = request.data
            cart_data, total_amount, address = OrderManager.fetch_cart(request, data)
            serializer_data = UserCartSerializer(cart_data, many=True).data
            serializer_data_address = AddressSerializer(address, many=True).data
            return Response({"result" : "success", "data":serializer_data, "total_amount":total_amount, "address":serializer_data_address}, 200)

        except Exception as err:
            return Response(str(err), 500)


class IncrementCartAction(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def post(request):
        try:
            data = request.data
            cart_data = OrderManager.cart_action(request, data)
            return Response({"result" : "success", "message":"action applied successfully"}, 200)

        except Exception as err:
            return Response(str(err), 500)


class PlaceOrderBeforePayment(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def post(request):
        try:
            data = request.data
            cart_data = OrderManager.check_order_before_payment(request, data)
            return Response({"result" : "success", "message":"Your order placed successfully"}, 200)

        except Exception as err:
            return Response(str(err), 500)



class PlaceOrderAfterPayment(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def post(request):
        try:
            data = request.data
            check_order = OrderManager.check_order_after_payment(request, data)
            return Response({"result" : "success", "message":"Your order placed successfully"}, 200)

        except Exception as err:
            return Response(str(err), 500)


class FetchCustomerApp(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            order_details = OrderManager.get_orders_customer(request, data)
            serializer_data = OrderSerializer(order_details, many=True).data
            return Response({"result" : "success", "data":serializer_data}, 200)

        except Exception as err:
            return Response(str(err), 500)


class fetchNotificationUser(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            order_details = OrderManager.get_orders_customer(request, data)
            serializer_data = OrderSerializer(order_details, many=True).data
            return Response({"result" : "success", "data":serializer_data}, 200)

        except Exception as err:
            return Response(str(err), 500)

class SetReviewRating(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def post(request):
        try:
            data = request.data
            order_review = OrderManager.add_review_in_order(request, data)
            return Response({"result" : "success", "message":"Thank you! Your review has been successfully submitted."}, 200)

        except Exception as err:
            return Response(str(err), 500)


