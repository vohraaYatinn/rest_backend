import jwt
from rest_framework.response import Response
from rest_framework.views import APIView

from menu.serializers import MenuItemSerializer, CategoryOnlySerializer, MenuRecommendationSerializer
from usersApp.custom_permission import IsAdminAuth, IsUserAuth
from usersApp.manager import CustomerManager
from usersApp.serializers import UserSerializer, UserAddressSerializer, UserOnlyAddressSerializer, \
    AddressUserSerializer, UserSingleSerializer, getNotificationSerializer


class getAdminLogin(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data
            user_exist = CustomerManager.get_admin_login(data)
            serialized_data = UserSerializer(user_exist).data
            payload = {
                'user': user_exist.phone_number
            }
            token = jwt.encode(payload, 'secretKeyRight34', algorithm='HS256')
            return Response({"result": "success", "user": serialized_data, "token": token},
                            200)

        except Exception as err:
            return Response(str(err), 500)


class getCustomer(APIView):
    permission_classes = [IsAdminAuth]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            get_all_customers = CustomerManager.get_customer_list(data)
            serialized_data = UserAddressSerializer(get_all_customers, many=True).data
            return Response({"result": "success", "data": serialized_data}, 200)

        except Exception as err:
            return Response(str(err), 500)

    @staticmethod
    def post(request):
        try:
            data = request.data
            CustomerManager.action_customer(data)
            return Response({"result": "success", "message": "Action applied on customer successfully"}, 200)

        except Exception as err:
            return Response(str(err), 500)



class AdminCharts(APIView):
    permission_classes = [IsAdminAuth]

    @staticmethod
    def get(request):
        try:
            data = request.data
            admin_charts_data = CustomerManager.get_admin_charts(data)
            return Response({"result": "success", "data": admin_charts_data}, 200)

        except Exception as err:
            return Response(str(err), 500)


class getAdminDashboard(APIView):
    permission_classes = [IsAdminAuth]

    @staticmethod
    def get(request):
        try:
            data = request.data
            get_dashboard_data = CustomerManager.get_dashboard_data(data)
            return Response({"result": "success", "data": get_dashboard_data}, 200)

        except Exception as err:
            return Response(str(err), 500)


class IsRestAvailable(APIView):
    permission_classes = [IsAdminAuth]

    @staticmethod
    def get(request):
        try:
            data = request.data
            order_summary = CustomerManager.get_rest_status(data)
            return Response({"result": "success", "data": order_summary}, 200)

        except Exception as err:
            return Response(str(err), 500)

    @staticmethod
    def post(request):
        try:
            data = request.data
            order_summary = CustomerManager.change_rest_status(data)
            return Response({"result": "success", "data": order_summary}, 200)

        except Exception as err:
            return Response(str(err), 500)


class singleCustomerFetch(APIView):
    permission_classes = [IsAdminAuth]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            customer_detail = CustomerManager.get_single_customer_detail(data)
            serialized_data = UserSingleSerializer(customer_detail).data
            return Response({"result": "success", "data": serialized_data}, 200)

        except Exception as err:
            return Response(str(err), 500)


# --------------- customer --------------------


class SignupCustomer(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data.get("inputValues", None)
            signup_customer = CustomerManager.signup_customer(data)
            serialized_data = UserSerializer(signup_customer).data
            payload = {
                'user': signup_customer.id
            }
            token = jwt.encode(payload, 'secretKeyRight34', algorithm='HS256')
            return Response({"result": "success", "message": "signup successful", "user": serialized_data, "token": token}, 200)

        except Exception as err:
            return Response(str(err), 500)


class LoginCustomer(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data.get("inputValues", None)
            user_exist = CustomerManager.login_user_customer(data)
            serialized_data = UserSerializer(user_exist).data
            payload = {
                'user': user_exist.id
            }
            token = jwt.encode(payload, 'secretKeyRight34', algorithm='HS256')
            return Response({"result": "success","message":"login successful", "user": serialized_data, "token": token},
                            200)
        except Exception as err:
            return Response(str(err), 500)


class CustomerAppDashboard(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def get(request):
        try:
            data = request.data
            dashboard_data = CustomerManager.fetch_dashboard_data(request, data)
            user_serialized_data = UserOnlyAddressSerializer(dashboard_data['req_user']).data
            recommended_serialized_data = MenuRecommendationSerializer(dashboard_data['recommended_order'], many=True).data
            all_categories_serialized_data = CategoryOnlySerializer(dashboard_data['all_categories'], many=True).data
            return Response({"result": "success", "data": {
                "user":user_serialized_data,
                "order":recommended_serialized_data,
                "category":all_categories_serialized_data,
            }},
                            200)
        except Exception as err:
            return Response(str(err), 500)


class getCustomerAddresses(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def get(request):
        try:
            data = request.data
            req_address = CustomerManager.get_customer_address(request, data)
            serialized_data = AddressUserSerializer(req_address, many=True).data
            return Response({"result": "success", "data": serialized_data},
                            200)
        except Exception as err:
            return Response(str(err), 500)

class addNewAddressCustomer(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def post(request):
        try:
            data = request.data.get("inputValues", None)
            CustomerManager.add_new_customer_address(request, data)
            return Response({"result": "success", "message": "New Address has been added successfully"},
                            200)
        except Exception as err:
            return Response(str(err), 500)

class deleteAddressCustomer(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def post(request):
        try:
            data = request.data
            CustomerManager.delete_customer_address(request, data)
            return Response({"result": "success", "message": "Address deleted successfully"},
                            200)
        except Exception as err:
            return Response(str(err), 500)


class defaultAddress(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def post(request):
        try:
            data = request.data
            CustomerManager.change_default_address(request, data)
            return Response({"result": "success", "message": "Default Address changed successfully"},
                            200)
        except Exception as err:
            return Response(str(err), 500)



class personalProfile(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def get(request):
        try:
            data = request.data
            req_user = CustomerManager.personal_profile(request, data)
            serialized_data = UserSerializer(req_user).data
            return Response({"result": "success", "data": serialized_data},
                            200)
        except Exception as err:
            return Response(str(err), 500)


    @staticmethod
    def post(request):
        try:
            data = request.data.get("inputValues", None)
            req_user = CustomerManager.edit_personal_profile(request, data)
            serialized_data = UserSerializer(req_user).data
            return Response({"result": "success", "data": serialized_data},
                            200)
        except Exception as err:
            return Response(str(err), 500)



class getUserNotification(APIView):
    permission_classes = [IsUserAuth]

    @staticmethod
    def get(request):
        try:
            data = request.data
            req_notification = CustomerManager.get_notification_user(request, data)
            serialized_data = getNotificationSerializer(req_notification, many=True).data
            return Response({"result": "success", "data": serialized_data},
                            200)
        except Exception as err:
            return Response(str(err), 500)



class makePassword(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data
            req_notification = CustomerManager.make_password(request, data)
            return Response({"result": "success", "message": "serialized_data"},
                            200)
        except Exception as err:
            return Response(str(err), 500)

