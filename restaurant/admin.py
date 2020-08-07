from django.contrib import admin

# Register your models here.
from restaurant.models import Restaurant, FavoriteRestaurant, BlackListedRestaurant

admin.site.register([Restaurant, FavoriteRestaurant, BlackListedRestaurant])
