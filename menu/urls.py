from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, MenuItemViewSet, MenuView, CategoryView, ChangeAvailablity, DeleteCategoryView, \
    SingleMenuItem, fetchAllMenuItems, fetchMenuByCategory, checkRestOnline

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'menu-items', MenuItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'get-category/', CategoryView.as_view(), name="get-category"),
    path(r'get-menu/', MenuView.as_view(), name="manage-menu"),
    path(r'add-menu-item/', MenuView.as_view(), name="manage-menu"),
    path(r'add-category/', CategoryView.as_view(), name="add-category"),
    path(r'delete-category/', DeleteCategoryView.as_view(), name="delete-category"),
    path(r'change-availability/', ChangeAvailablity.as_view(), name="change-availability"),

    # customer
    path(r'single-menu-item/', SingleMenuItem.as_view(), name="single-menu-item"),
    path(r'get-all-menu-items/', fetchAllMenuItems.as_view(), name="get-all-menu-items"),
    path(r'category-menu/', fetchMenuByCategory.as_view(), name="category-menu"),
    path(r'check-rest-online/', checkRestOnline.as_view(), name="check-rest-online"),

]
