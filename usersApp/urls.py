from django.urls import path, include
from rest_framework.routers import DefaultRouter

from usersApp.views import getCustomer, getAdminLogin, getAdminDashboard, AdminCharts, IsRestAvailable, SignupCustomer, \
    LoginCustomer, CustomerAppDashboard, getCustomerAddresses, addNewAddressCustomer, deleteAddressCustomer, \
    defaultAddress, personalProfile, singleCustomerFetch

urlpatterns = [
    # ------------ admin ----------------
    path(r'get-admin-login/', getAdminLogin.as_view(), name="get-admin-login"),
    path(r'get-customer/', getCustomer.as_view(), name="get-customer"),
    path(r'action-customer/', getCustomer.as_view(), name="action-customer"),
    path(r'get-admin-dashboard/', getAdminDashboard.as_view(), name="get-admin-dashboard"),
    path(r'admin-charts/', AdminCharts.as_view(), name="admin-charts"),
    path(r'is_rest_available/', IsRestAvailable.as_view(), name="is_rest_available"),
    path(r'single-customer-fetch/', singleCustomerFetch.as_view(), name="single-customer-fetch"),

    # -------------- customer -------------
    path(r'sign-up-customer/', SignupCustomer.as_view(), name="sign-up-customer"),
    path(r'login-customer/', LoginCustomer.as_view(), name="login-customer"),
    path(r'fetch-dashboard-customer/', CustomerAppDashboard.as_view(), name="fetch-dashboard-customer"),
    path(r'manage-address/', getCustomerAddresses.as_view(), name="manage-address"),
    path(r'add-new-address/', addNewAddressCustomer.as_view(), name="add-new-address"),
    path(r'delete-address/', deleteAddressCustomer.as_view(), name="delete-address"),
    path(r'default-address/', defaultAddress.as_view(), name="default-address"),
    path(r'fetch-user-details/', personalProfile.as_view(), name="fetch-user-details"),
    path(r'edit-user-details/', personalProfile.as_view(), name="edit-user-details"),
    path(r'fetch-user-notification/', personalProfile.as_view(), name="fetch-user-notification"),

]



