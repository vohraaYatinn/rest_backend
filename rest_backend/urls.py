from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/menu/', include('menu.urls')),           # URLs for the menu app
    path('api/orders/', include('orders.urls')),       # URLs for the orders app
    path('api/users/', include('usersApp.urls')),         # URLs for the users app
    path('api/restaurant/', include('restaurant.urls')), # URLs for the restaurant app
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)