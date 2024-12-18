from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu/', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.IntegerField( default=0)
    is_available = models.BooleanField(default=True)
    is_buy_one = models.BooleanField(default=False)
    side_on = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class MenuRecommendation(models.Model):
    menu = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='recommended_menu')
