from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderView, OrderStatusChange, FetchSingleOrder, AddToCart, FetchCustomerCart, \
    IncrementCartAction, FetchCustomerApp, fetchNotificationUser, SetReviewRating, PlaceOrderBeforePayment, \
    PlaceOrderAfterPayment, changeOrderAttended

router = DefaultRouter()
router.register(r'orders', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path(r'fetch-order/', OrderView.as_view(), name="fetch-order"),
    path(r'fetch-single-order/', FetchSingleOrder.as_view(), name="fetch-single-order"),
    path(r'order-status-change/', OrderStatusChange.as_view(), name="order-status-change"),
    path(r'order-change-attended/', changeOrderAttended.as_view(), name="order-change-attended"),

    # customer
    path(r'add-to-cart/', AddToCart.as_view(), name="add-to-cart"),
    path(r'fetch-customer-cart/', FetchCustomerCart.as_view(), name="fetch-customer-cart"),
    path(r'customer-cart-action/', IncrementCartAction.as_view(), name="customer-cart-action"),
    path(r'place-order-before-payment/', PlaceOrderBeforePayment.as_view(), name="place-order"),
    path(r'fetch-customer-order/', FetchCustomerApp.as_view(), name="fetch-customer-order"),
    path(r'get-single-order/', FetchCustomerApp.as_view(), name="get-single-order"),
    path(r'get-order-notification/', fetchNotificationUser.as_view(), name="get-order-notification"),
    path(r'add-new-review/', SetReviewRating.as_view(), name="add-new-review"),
    path(r'place-order-after-payment/', PlaceOrderAfterPayment.as_view(), name="order-after-payment"),

]
