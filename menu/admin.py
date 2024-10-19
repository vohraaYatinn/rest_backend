from .models import Category, MenuItem, MenuRecommendation
from django.contrib import admin

# Register your models here.
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(MenuRecommendation)
